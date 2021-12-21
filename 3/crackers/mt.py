import tqdm

from typing import Union, Literal

import generators.mt
from client import CasinoClient, CasinoAccountModel
from .base import BaseCracker

#
def unapply_transform(transformed: int) -> int:
    val = transformed ^ (transformed >> 18)
    val = val ^ ((val << 15) & 0xefc60000)

    for i in range(7):
        val ^= (val << 7) & 0x9d2c5680

    for i in range(3):
        val = val ^ (val >> 11)

    return val


class MTCracker(BaseCracker):

    def __init__(self, player_id: Union[str, int], algo: Literal['Mt', 'BetterMt']):
        self.player_id = player_id
        self.algo = algo
        self.account = CasinoClient.create_account(self.player_id)

    def crack(self, money_to_generate: int) -> CasinoAccountModel:
        bar_size = 624 + int(money_to_generate / 250000)

        bar = tqdm.trange(bar_size)
        bar.set_description('Sending requests to casino')

        bet_results = []

        for i in range(624):
            bet_results.append(CasinoClient.make_bet(self.player_id, self.algo, 1, 5))
            bar.update(1)

        bar.set_description('Injecting results')

        bet_numbers = [r.real_number for r in bet_results]
        money = bet_results[-1].account.money
        bar.update(20)

        solver = generators.mt.MTGenerator(0)
        solver.set_state_with_index(list(map(unapply_transform, bet_numbers)), 624)
        bar.update(40)

        bar.set_description('Generating money')
        while money <= money_to_generate:
            res = CasinoClient.make_bet(self.player_id, self.algo, 300, solver.next())
            money = res.account.money
            bar.update(1)

        if bar.n != bar_size:
            bar.update(bar_size - bar.n)

        bar.set_description('Done')
        return res.account

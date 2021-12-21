import ctypes
from typing import Union, Any, Tuple, Generator

import tqdm

from client import CasinoClient, CasinoAccountModel
from .base import BaseCracker


def mod_with_negative(a: int, b: int):
    return a - int(a / b) * b


class LcgCracker(BaseCracker):
    def __init__(
            self,
            player_id: Union[str, int],
            modulus: int
    ):
        self.player_id = player_id
        self.modulus = modulus

        self.account = CasinoClient.create_account(self.player_id)

    def get_increment_and_multiplier(self, states: Tuple[int, ...]) -> Tuple[int, ...]:
        multiplier = self.get_multiplier(states)
        mod_part = states[1] - states[0] * multiplier
        return multiplier, mod_with_negative(mod_part, self.modulus)

    def get_multiplier(self, states: Tuple[int, ...]) -> int:
        mod_part = (states[2] - states[1]) * pow(states[1] - states[0], -1, self.modulus)
        return mod_with_negative(mod_part, self.modulus)

    def get_next_value(self, multiplier: int, increment: int, last_state: int) -> Generator[int, None, None]:
        while True:
            mod_part = multiplier * last_state + increment
            last_state = mod_with_negative(mod_part, self.modulus)
            yield last_state  # to signed

    def crack(self, money_to_generate: int) -> CasinoAccountModel:
        bar_size = 9 + int(money_to_generate / 250000)
        bar = tqdm.trange(bar_size)
        bar.set_description('Sending requests to casino')

        three_results = (
            CasinoClient.make_bet(self.player_id, 'Lcg', 1, 1),
            CasinoClient.make_bet(self.player_id, 'Lcg', 1, 1),
            CasinoClient.make_bet(self.player_id, 'Lcg', 1, 1)
        )
        bar.update(3)
        bar.set_description('Injecting results')

        states = tuple(bet.real_number for bet in three_results)
        m, i = self.get_increment_and_multiplier(states)
        bar.update(3)

        money = 0
        generator = self.get_next_value(m, i, states[-1])
        bar.update(3)

        bar.set_description('Generating money')

        while money <= money_to_generate:
            next_value = ctypes.c_int32(next(generator) | 0).value
            res = CasinoClient.make_bet(self.player_id, 'Lcg', 500, next_value)
            money = res.account.money
            bar.update(1)

        if bar.n != bar_size:
            bar.update(bar_size - bar.n)

        bar.set_description('Done')
        bar.close()
        return res.account

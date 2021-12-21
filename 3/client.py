import requests
import datetime

from typing import Union, Literal
from pydantic import BaseModel, validator, Field


class CasinoClientPaths:
    BASE_URL = 'http://95.217.177.249'

    CREATE_ACC = BASE_URL + '/casino/createacc?id={id}'
    MAKE_BET = BASE_URL + '/casino/play{mode}?id={player_id}&bet={bet}&number={number}'


class CasinoAccountModel(BaseModel):
    id: str
    money: int
    deletion_time: datetime.datetime = Field(alias='deletionTime')


class MakeBetGET(BaseModel):
    message: str
    account: CasinoAccountModel
    real_number: int = Field(alias='realNumber')


class CasinoClient:
    @staticmethod
    def create_account(player_id: Union[str, int]) -> CasinoAccountModel:
        response = requests.get(CasinoClientPaths.CREATE_ACC.format(id=player_id))
        if response.status_code != 201:
            raise Exception(f'failed create account, player_id={player_id}')
        return CasinoAccountModel(**response.json())

    @staticmethod
    def make_bet(
            player_id: Union[str, int],
            mode: Literal['Lcg', 'Mt', 'BetterMt'],
            bet: int,
            number: int
    ) -> MakeBetGET:
        response = requests.get(CasinoClientPaths.MAKE_BET.format(
            mode=mode,
            player_id=player_id,
            bet=bet,
            number=number
        ))
        if response.status_code != 200:
            raise Exception('failed make bet')
        return MakeBetGET(**response.json())

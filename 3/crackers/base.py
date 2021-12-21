from abc import ABC, abstractmethod

from client import CasinoAccountModel


class BaseCracker(ABC):
    @abstractmethod
    def crack(self, money: int) -> CasinoAccountModel: ...

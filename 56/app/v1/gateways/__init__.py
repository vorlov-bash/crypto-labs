from dependency_injector import containers, providers
from typing import Union
from .sqlite import SQLiteProxy
from config import CONFIG


class GatewaysContainer(containers.DeclarativeContainer):
    sqlite: Union[providers.Singleton, SQLiteProxy] = providers.Singleton(
        SQLiteProxy,
        file_path=CONFIG.v1.sqlite_path.as_posix()
    )

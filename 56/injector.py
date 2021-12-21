from typing import Union

from dependency_injector import containers, providers
from app.v1.injector import V1App


class MainContainer(containers.DeclarativeContainer):
    v1: Union[providers.Container, V1App] = providers.Container(V1App)

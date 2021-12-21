from dependency_injector import containers, providers
from typing import Union

from .gateways import GatewaysContainer
from .models import ModelsContainer


class V1App(containers.DeclarativeContainer):
    gateways: Union[providers.Container, GatewaysContainer] = providers.Container(GatewaysContainer)
    models: Union[providers.Container, ModelsContainer] = providers.Container(ModelsContainer, gateways=gateways)

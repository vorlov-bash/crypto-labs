from dependency_injector import containers, providers

from typing import TYPE_CHECKING, Union

from .user import UserService
from ..crypt import EncryptService, DecryptService
from config import CONFIG

if TYPE_CHECKING:
    from ..gateways import GatewaysContainer


class ModelsContainer(containers.DeclarativeContainer):
    gateways: Union[providers.DependenciesContainer, 'GatewaysContainer'] = providers.DependenciesContainer()

    sf = gateways.sqlite.provided.session
    encrypt: Union[providers.Singleton, EncryptService] = providers.Singleton(
        EncryptService,
        CONFIG.v1.secret_key
    )

    decrypt: Union[providers.Singleton, DecryptService] = providers.Singleton(
        DecryptService,
        CONFIG.v1.secret_key
    )

    user: Union[providers.Singleton, UserService] = providers.Singleton(
        UserService,
        session_factory=sf,
        encrypt_service=encrypt,
        decrypt_service=decrypt
    )



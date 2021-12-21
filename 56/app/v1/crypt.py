import base64

from typing import Union, Optional, Literal, Tuple, List
from nacl import pwhash, secret, utils


class EncryptService:
    def __init__(
            self,
            secret_key: Union[bytes, str],
            argon_type: Optional[Literal['argon2i', 'argon2id']] = 'argon2i'
    ):
        self.argon = getattr(pwhash, argon_type)
        self.opslimit = self.argon.OPSLIMIT_SENSITIVE
        self.memlimit = self.argon.MEMLIMIT_SENSITIVE

        if isinstance(secret_key, str):
            secret_key = secret_key.encode()
        self.secret_key = secret_key

    def encrypt_data_with_secret(self, data: Union[str, bytes]) -> str:
        if isinstance(data, str):
            data = data.encode()

        box = secret.SecretBox(self.secret_key)
        nonce = utils.random(secret.SecretBox.NONCE_SIZE)
        return base64.b64encode(box.encrypt(data, nonce)).decode()

    def encrypt_plaintext_password(self, user_password: str) -> str:
        argon_hash = self.argon.str(user_password.encode(),
                                    opslimit=self.opslimit,
                                    memlimit=self.memlimit)

        return self.encrypt_data_with_secret(argon_hash)

    @staticmethod
    def get_new_dek():
        return secret.random()

    def encrypt_data_with_dek(
            self,
            data: Union[str, bytes],
            custom_dek: Optional[Union[str, bytes]] = None,
            custom_ciphered_dek: Optional[Union[str, bytes]] = None
    ) -> Tuple[str, str]:

        if not custom_dek and custom_ciphered_dek:
            raise Exception

        if isinstance(custom_dek, str):
            custom_dek = custom_dek.encode()

        if isinstance(custom_ciphered_dek, str):
            custom_ciphered_dek = custom_ciphered_dek.encode()

        dek = custom_dek or secret.random()
        ciphered_dek = custom_ciphered_dek or self.encrypt_data_with_secret(dek)

        if isinstance(data, str):
            data = data.encode()

        box = secret.SecretBox(dek)
        nonce = utils.random(secret.SecretBox.NONCE_SIZE)

        return ciphered_dek, base64.b64encode(box.encrypt(data, nonce)).decode()

    def encrypt_data_chunk(self, data_chunk: List[Union[str, bytes]]) -> Tuple[str, List[str]]:
        dek = self.get_new_dek()
        ciphered_dek = self.encrypt_data_with_secret(dek)

        for i in range(len(data_chunk)):
            if isinstance(data_chunk[i], str):
                data_chunk[i] = data_chunk[i].encode()
            _, data_chunk[i] = self.encrypt_data_with_dek(data_chunk[i], dek, ciphered_dek)

        return ciphered_dek, data_chunk


class DecryptService:
    def __init__(
            self,
            secret_key: Union[bytes, str],
            argon_type: Optional[Literal['argon2i', 'argon2id']] = 'argon2i'
    ):
        self.argon = getattr(pwhash, argon_type)
        self.opslimit = self.argon.OPSLIMIT_SENSITIVE
        self.memlimit = self.argon.MEMLIMIT_SENSITIVE

        if isinstance(secret_key, str):
            secret_key = secret_key.encode()
        self.secret_key = secret_key

    def decrypt_data_with_secret(self, b64_data: Union[str, bytes]) -> bytes:
        if isinstance(b64_data, str):
            b64_data = b64_data.encode()

        data = base64.b64decode(b64_data)

        box = secret.SecretBox(self.secret_key)
        return box.decrypt(data)

    def decrypt_data_with_ciphered_dek(
            self,
            b64_data: Union[str, bytes],
            custom_dek: Optional[Union[str, bytes]] = None,
            ciphered_b64_dek: Optional[Union[str, bytes]] = None
    ) -> str:
        if bool(custom_dek) == bool(ciphered_b64_dek):  # xor args
            raise Exception

        if isinstance(custom_dek, str):
            custom_dek = custom_dek.encode()

        if isinstance(ciphered_b64_dek, str):
            ciphered_b64_dek = ciphered_b64_dek.encode()

        dek = custom_dek or self.decrypt_data_with_secret(ciphered_b64_dek)

        if isinstance(b64_data, str):
            b64_data = b64_data.encode()

        data = base64.b64decode(b64_data)

        box = secret.SecretBox(dek)
        return box.decrypt(data).decode()

    def decrypt_data_chunk(
            self,
            data_chunk: List[Union[str, bytes]],
            ciphered_b64_dek: Union[str, bytes]
    ) -> List[str]:
        dek = self.decrypt_data_with_secret(ciphered_b64_dek)
        for i in range(len(data_chunk)):
            if isinstance(data_chunk[i], str):
                data_chunk[i] = data_chunk[i].encode()
            data_chunk[i] = self.decrypt_data_with_ciphered_dek(data_chunk[i], custom_dek=dek)
        return data_chunk

    def verify_plaintext_with_hash(self, b64_hash_message: Union[str, bytes], user_password: str) -> bool:
        argon_hash = self.decrypt_data_with_secret(b64_hash_message)

        return self.argon.verify(argon_hash, user_password.encode())

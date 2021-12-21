from pydantic import BaseModel, validator
from typing import Optional, Literal, Union
from yaml import safe_load
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve(strict=True).parent


class V1ConfigSchema(BaseModel):
    host: Optional[str] = 'localhost'
    port: Optional[int] = 9999

    secret_key: str
    sqlite_path: Optional[pathlib.Path] = BASE_DIR / 'sqlite.db'

    argon: Optional[Literal['argon2i', 'argon2id']]

    @validator('secret_key')
    def check_secret_key_len(cls, v):
        if len(v) != 32:
            raise ValueError('secret_key must be 32 length')
        return v


class ConfigSchema(BaseModel):
    version: Literal['v1']

    v1: Optional[V1ConfigSchema]


with open(BASE_DIR / 'config.yml', 'r') as yaml_stream:
    CONFIG = ConfigSchema(**safe_load(yaml_stream))

with open(BASE_DIR / 'weak_passwords', 'r') as file:
    WEAK_PASS_LIST = []

    for line in file.readlines():
        WEAK_PASS_LIST.append(line[:-1])


from pydantic import SecretStr, BaseSettings
from typing import List, AnyStr


class Setting(BaseSettings):
    bot_token: SecretStr

    card_number: AnyStr = '5466-6575-5437-5876'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Setting()

import os
from pydantic import BaseSettings, SecretStr

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
env_dir = os.path.abspath(os.path.join(parent_dir, '.env'))


class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    MONGO_USERNAME: SecretStr
    MONGO_PASSWORD: SecretStr
    MONGO_CLUSTER: SecretStr
    OPENAI_API_KEY: SecretStr
    SERP_API_KEY: SecretStr
    CURRENT_SCHEMA_VERSION: int

    class Config:
        env_file = env_dir
        env_file_encoding = 'utf-8'


config = Config()


if __name__ == '__main__':
    print(config)

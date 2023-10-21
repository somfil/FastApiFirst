from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', extra='allow')
    url: str = Field('db_url', alias='DB_URL')


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', extra='allow')
    secret_key: str = Field('secret_key', alias='SECRET_KEY')
    algorithm: str = Field('algorithm', alias='JWT_ALGORITHM')
    access_token_lifetime: int = Field(15, alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_lifetime: int = Field(15, alias='REFRESH_TOKEN_EXPIRE_DAYS')


class Settings(BaseSettings):
    jwt: JWTSettings = JWTSettings()
    db_url: DBSettings = DBSettings()


settings = Settings()

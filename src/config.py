from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    TG_TOKEN: str
    TG_CHANNEL_ID: int
    VK_TOKEN: str
    VK_CHANNEL_ID: int

    OPENAI_KEY: str
    FUSION_BRAIN_API_KEY: str
    FUSION_BRAIN_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()

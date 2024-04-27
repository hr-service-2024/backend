from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class PostgresSettings(BaseConfigSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str


class JWTSettings(BaseConfigSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60


class FusionBrainSettings(BaseConfigSettings):
    FUSION_BRAIN_API_KEY: str
    FUSION_BRAIN_SECRET_KEY: str


class Settings(BaseConfigSettings):
    db: PostgresSettings = PostgresSettings()
    jwt: JWTSettings = JWTSettings()
    fusion_brain: FusionBrainSettings = FusionBrainSettings()

    TG_TOKEN: str
    TG_CHANNEL_ID: int
    VK_TOKEN: str
    VK_CHANNEL_ID: int
    OPENAI_KEY: str


settings = Settings()

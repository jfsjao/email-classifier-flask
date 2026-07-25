import os
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseConfig:
    SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY", "chave_secreta_flask")
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    GEMINI_API_URL: str | None = None


@dataclass(frozen=True)
class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


@dataclass(frozen=True)
class TestingConfig(BaseConfig):
    TESTING: bool = True
    DEBUG: bool = False


@dataclass(frozen=True)
class ProductionConfig(BaseConfig):
    DEBUG: bool = False


def get_config() -> type[BaseConfig]:
    env = os.getenv("FLASK_ENV", "development").lower()
    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    return configs.get(env, DevelopmentConfig)

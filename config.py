from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.
    """

    database_url: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates the DbConfig object from environment variables.

        postgresql+asyncpg://{user}:{password}@{host}/{database}
        """

        host = env.str("DB_HOST")
        password = env.str("DB_PASSWORD")
        user = env.str("DB_USER")
        database = env.str("DB_NAME")
        port = env.int("DB_PORT", 5432)

        database_url = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'

        return DbConfig(
            database_url=database_url
        )


@dataclass
class TgBotConfig:
    """
    Telegram bot configuration class.
    """

    token: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")

        return TgBotConfig(
            token=token
        )


@dataclass
class TONApiConfig:
    """
    Fernet configuration class.
    """

    key: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates the Fernet object from environment variables.
        """
        tonapi_key = env.str("TONAPI_KEY")

        return TONApiConfig(
            key=tonapi_key
        )


@dataclass
class EncryptionConfig:
    """
    Fernet configuration class.
    """

    encryption_key: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates the Fernet object from environment variables.
        """
        encryption_key = env.str("ENCRYPTION_KEY")

        return EncryptionConfig(
            encryption_key=encryption_key
        )


@dataclass
class AppConfig:
    server_url: str
    client_url: str

    @staticmethod
    def from_env(env: Env):
        server_url = env.str("SERVER_URL")
        client_url = env.str("CLIENT_URL")

        return AppConfig(
            server_url=server_url,
            client_url=client_url
        )


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.
    This class holds the other configuration classes, providing a centralized point of access for all settings.
    """

    # app: AppConfig
    tg_bot: TgBotConfig
    tonapi: TONApiConfig
    encryption: EncryptionConfig
    db: DbConfig
    app: AppConfig


def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBotConfig.from_env(env),
        tonapi=TONApiConfig.from_env(env),
        encryption=EncryptionConfig.from_env(env),
        db=DbConfig.from_env(env),
        app=AppConfig.from_env(env)
    )


config = load_config(".env")

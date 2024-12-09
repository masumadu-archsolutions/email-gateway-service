import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from app import constants


class BaseConfig(BaseSettings):
    # reminder: general application settings
    app_name: str = "Email Gateway"
    app_env: str = ""
    app_root: str = str(Path(__file__).parent)
    log_header: str = f"{app_name} Log"
    admin_mail_address: str = ""
    cors_origins: str = "*"
    # database config
    db_uri: str = ""
    # redis config
    redis_uri: str = ""
    # reminder: mail server config
    mail_server: str = ""
    mail_server_port: str = ""
    default_mail_sender: str = ""
    default_mail_sender_address: str = ""
    default_mail_sender_password: str = ""
    # keycloak configuration
    jwt_algorithms: list = ["HS256", "RS256"]
    jwt_public_key: str = ""
    keycloak_uri: str = ""
    keycloak_realm: str = ""
    # inter service http request
    internal_service_ssl: bool = True
    user_service_base_url: str = ""
    # kafka configuration
    kafka_bootstrap_servers: str = ""
    kafka_server_username: str = ""
    kafka_server_password: str = ""
    kafka_subscriptions: str = ""
    kafka_consumer_group: str = ""

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return self.db_uri

    class Config:
        env_file = ".env"
        extra = "allow"


class DevelopmentConfig(BaseConfig):
    pass


class UatConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    test_db_uri: str = ""

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return self.test_db_uri


def get_settings():
    load_dotenv(".env")
    config_cls_dict = {
        constants.DEVELOPMENT_ENVIRONMENT: DevelopmentConfig,
        constants.UAT_ENVIRONMENT: UatConfig,
        constants.PRODUCTION_ENVIRONMENT: ProductionConfig,
        constants.TESTING_ENVIRONMENT: TestingConfig,
    }
    config_name = os.getenv("APP_ENV", default=constants.DEVELOPMENT_ENVIRONMENT)
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()

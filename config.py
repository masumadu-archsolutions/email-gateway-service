import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from app import constants


class BaseConfig(BaseSettings):
    # general application settings
    app_name: str = "Email Gateway"
    app_alias: str = "email"
    app_env: str = ""
    app_root: str = str(Path(__file__).parent)
    log_header: str = f"{app_name} Log"
    maintainer_mail_address: str = ""
    cors_origins: str = "*"
    # database server configuration
    db_host: str = ""
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    db_port: int = 5432
    db_ssl: bool = True
    db_connection_pool: bool = True
    # redis server configuration
    redis_server: str = ""
    redis_port: int = 6379
    redis_password: str = ""
    # rabbitmq server configuration
    rmq_server: str = ""
    rmq_port: int = 5672
    rmq_user: str = ""
    rmq_password: str = ""
    rmq_vhost: str = ""
    # mail server configuration
    mail_server: str = ""
    mail_server_port: str = ""
    default_mail_sender: str = ""
    default_mail_sender_address: str = ""
    default_mail_sender_password: str = ""
    # keycloak configuration
    keycloak_uri: str = ""
    keycloak_realm: str = ""
    jwt_algorithms: list = ["HS256", "RS256"]
    jwt_public_key: str = ""
    # inter service http request
    internal_service_ssl: bool = True
    user_service_base_url: str = ""
    # kafka configuration
    kafka_bootstrap_servers: str = ""
    kafka_server_username: str = ""
    kafka_server_password: str = ""
    kafka_subscription: str = ""
    kafka_consumer_group: str = ""

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return "postgresql+psycopg2://{db_user}:{password}@{host}:{port}/{db_name}".format(  # noqa
            db_user=self.db_user,
            host=self.db_host,
            password=self.db_password,
            port=self.db_port,
            db_name=self.db_name,
        )

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
    test_db_host: str = ""
    test_db_user: str = ""
    test_db_password: str = ""
    test_db_name: str = ""
    test_db_port: str = ""
    db_ssl: bool = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return "postgresql+psycopg2://{db_user}:{password}@{host}:{port}/{db_name}".format(  # noqa
            db_user=self.test_db_user,
            host=self.test_db_host,
            password=self.test_db_password,
            port=self.test_db_port,
            db_name=self.test_db_name,
        )


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

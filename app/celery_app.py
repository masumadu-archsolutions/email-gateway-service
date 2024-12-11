from logging.config import dictConfig

from celery.signals import setup_logging

from app import init_celery, log_config

celery = init_celery()
celery.config_from_object("celeryconfig")


@setup_logging.connect
def config_loggers(*args, **kwargs):
    dictConfig(log_config())

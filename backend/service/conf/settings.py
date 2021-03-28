# pylint: disable=W0401,C0413,W0614

import os
from typing import Optional

from pydantic import BaseSettings

APP_NAME = os.getenv('APP_NAME', 'Server')
APP_VERSION = os.getenv('APP_VERSION', '0.1.0')


class Level:
    DEV = 'dev'
    PROD = 'prod'


RUN_LEVEL = os.getenv('RUN_LEVEL', Level.PROD)
DEBUG = RUN_LEVEL == Level.DEV


class ServiceSettings(BaseSettings):
    MAX_LIMIT: int = 20

    class Config:
        env_prefix = 'APP_'


service_settings = ServiceSettings()


class CelerySettings(BaseSettings):
    TASKS_DB: str = '14'
    RESULT_DB: str = '15'

    class Config:
        env_prefix = 'APP_CELERY_'


celery_settings = CelerySettings()


class PostgresSettings(BaseSettings):
    NAME: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str

    class Config:
        env_prefix = 'APP_PG_'


class RedisSettings(BaseSettings):
    HOST: str
    PORT: str
    USER: Optional[str]
    PASSWORD: Optional[str]

    class Config:
        env_prefix = 'APP_REDIS_'


pg_settings = PostgresSettings()
redis_settings = RedisSettings()


def uri_maker(conf_object, driver):
    def make_uri(
        user: Optional[str] = conf_object.USER,
        password: Optional[str] = conf_object.PASSWORD,
        host: str = conf_object.HOST,
        port: str = conf_object.PORT,
        db: Optional[str] = getattr(conf_object, 'NAME', None),
    ) -> str:
        if user:
            if password:
                auth = f'{user}:{password}'
            else:
                auth = user
            auth += '@'
        else:
            auth = ''

        connection_string = f'{driver}://{auth}{host}:{port}'
        if db:
            connection_string += f'/{db}'
        return connection_string

    return make_uri


make_pg_uri = uri_maker(pg_settings, 'postgresql+psycopg2')
make_redis_uri = uri_maker(redis_settings, 'redis')
PG_URI = make_pg_uri()
REDIS_URL = make_redis_uri()

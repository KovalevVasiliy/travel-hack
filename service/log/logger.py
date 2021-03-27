import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Union

from pydantic import BaseSettings, Field, validator

from conf import DEBUG, RUN_LEVEL, Level
from log.context import current_context

DATE_FMT = '%Y-%m-%dT%H:%M:%S%Z'

logging.lastResort = None
logging.raiseExceptions = DEBUG

LEVELS = {
    Level.DEV: logging.DEBUG,
}


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.actor_id = current_context.get_actor_id()  # type:ignore
        record.actor_type = current_context.get_actor_type()  # type:ignore
        record.request_id = current_context.get_request_id()  # type:ignore
        return True


class LoggingConfig(BaseSettings):
    # actual values of LEVEL == logging.[INFO,DEBUG]
    LEVEL: Union[int, str] = Field(default_factory=lambda: LEVELS.get(RUN_LEVEL, logging.INFO))
    NAME: str = 'app'
    FILENAME: str = '/mnt/log/app.log'

    class Config:
        env_prefix = 'LOG_'

    @validator('LEVEL')
    # pylint: disable=no-self-argument ; pylint is stupid
    def validate_level(cls, value: Any) -> Any:  # pragma: no cover
        if isinstance(value, int):  # if level has already been set
            return value

        level = logging.getLevelName(value)
        if isinstance(level, str) and level.startswith('Level '):
            raise ValueError(f'Invalid logging level <{value}>')
        return level


config = LoggingConfig()
context_filter = ContextFilter()
formatter = logging.Formatter(
    fmt='%(asctime)s %(name)s:%(levelname)s %(request_id)s:%(actor_type)s:%(actor_id)s %(message)s',
    datefmt=DATE_FMT,
)
file_handler = RotatingFileHandler(
    filename=config.FILENAME,
    encoding='utf-8',
    maxBytes=1024 * 1024 * 50,  # 50 megabytes
    backupCount=9,  # 10 logs, 50 megabytes each - half a gb
)
file_handler.setFormatter(formatter)

# Disabling unused info gathering
# pylint: disable=protected-access
logging._srcfile = None  # type:ignore
logging.logThreads = False
logging.logProcesses = False
logging.logMultiprocessing = False

log = logging.getLogger(config.NAME)
log.addFilter(context_filter)
log.addHandler(file_handler)

logging.getLogger().addFilter(context_filter)
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s %(name)s:%(levelname)s %(message)s', datefmt=DATE_FMT,
)
log.setLevel(config.LEVEL)

log.info('Initialized logging with level: %s, filename: %s', config.LEVEL, config.FILENAME)

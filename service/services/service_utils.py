# NOTE: in the future, all files at this level should be moved to separate library

import functools
from datetime import date, datetime, time
from typing import Any, Callable, List, Type, TypeVar, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session

from conf import service_settings
from log import log
from utils.types import HasID

from .api import Error, NotFoundError  # pylint: disable=E0402

T = TypeVar('T', bound=HasID)


def paginate(query: Query, model: Type[T], offset: int, limit: int) -> List[T]:
    if limit > service_settings.MAX_LIMIT:
        raise Error(f'Maximum limit is {service_settings.MAX_LIMIT}!')
    return query.order_by(model.id).offset(offset).limit(limit).all()


def raise_on_none(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        if result is None:
            raise NotFoundError('Not found')
        return result

    return decorated


datetime_type = Union[datetime, date]


def normalize_date(dt: datetime_type) -> datetime:
    if isinstance(dt, date):
        dt = datetime.combine(dt, time())
    return dt


def handle_db_error(
    session: Session, exc: IntegrityError, obj: Any, auto_rollback: bool = True
) -> Exception:
    if auto_rollback:
        try:
            session.rollback()
        except:  # pylint: disable=bare-except
            log.exception('Could not auto rollback on db error!')

    exc_msg: str = str(exc.args[0])

    #if 'unique constraint \"operators_email_key\"' in exc_msg:
    #    return Error(f"""Operator with email "{getattr(obj, 'email', None)}" already exists""")
    return exc

from typing import Generator, Optional

from sqlalchemy.orm import Session as SessionType

from database import Session
#from log import log


def get_db() -> Generator[SessionType, None, None]:  # pragma: no cover
    db: Optional[SessionType] = None
    try:
        db = Session()  # type: ignore
        yield db
    except:  # pylint: disable=bare-except
        pass
        #log.exception('Could not create db session!')
    else:
        try:
            db.commit()
        except:  # pylint: disable=bare-except
            #log.exception('Could not commit transaction on end of request!')
            db.rollback()
    finally:
        if db:
            Session.remove()

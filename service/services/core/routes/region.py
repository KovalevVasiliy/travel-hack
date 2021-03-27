from typing import Any, List, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from crud import get_pop_region_categories
from database import CategoryModel
from services.api import Error, responses
from services.dependencies import get_db

from . import api


@api.get('/region/top-categories', response_model=List[Any], responses=responses)
def top_categories_by_region(city: str, db: Session = Depends(get_db)) -> List[Any]:
    return get_pop_region_categories(db, city)

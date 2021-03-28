from datetime import date, datetime
from typing import List, Union, Dict, Any

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from crud.region import get_region_by_name
from database import Location, Tour, Category, Region
from services.api import responses
from services.dependencies import get_db
from . import api


class CategoryWeight(BaseModel):
    id: int
    weight: int


class PlanRequest(BaseModel):
    date_from: date
    date_to: date
    city: str
    categories: List[CategoryWeight]


class Coordinates(BaseModel):
    lat: str
    lon: str


class Guide(BaseModel):
    name: str
    avatar: str


class PlaceBlock(BaseModel):
    name: str
    description: str
    image: str
    coords: Coordinates
    images_gallery: List[str]
    likes_count: int
    is_liked: bool


class TourBlock(PlaceBlock):
    price: str
    places: List[PlaceBlock]
    guide: Guide


class Block(BaseModel):
    time: datetime
    type: str
    block: Union[PlaceBlock, TourBlock]  # max len: 3


class DayPlan(BaseModel):
    date: date
    blocks: List[Block]


@api.post('/plan', response_model=DayPlan, responses=responses)
def plan_trip(request: PlanRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    top_categories = [str(cat.id) for cat in request.categories.sort(key=lambda category: category.weight, reverse=True)[:5]]
    region_id = get_region_by_name(db, request.city)
    places = db.query(Location).filter(Location.type_id.op('?|')(top_categories), Location.local_id == region_id)
    return places.fetchall()

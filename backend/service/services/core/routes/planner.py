from collections import defaultdict
from datetime import date, datetime, timedelta, time
from random import choice, randint, shuffle, choices
from typing import Any, Dict, List, Optional, Union

from fastapi import Depends
from pydantic import BaseModel, parse_obj_as
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.orm import Session

from crud.region import get_region_by_name
from database import Location, Tour
from services.api import responses
from services.dependencies import get_db

from . import api
from .region import images


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
    time: Optional[datetime] = None
    type: str
    block: Union[PlaceBlock, TourBlock]  # max len: 3


class DayPlan(BaseModel):
    date: date
    blocks: List[Block]


MAX_PLACES_PER_DAY = 3


def process_place(place) -> Block:
    try:
        place['object_coord']
    except:
        type_ = 'tour'
    else:
        type_ = 'location'

    prefix = 'tour' if type_ == 'tour' else 'object'

    data = {
        'name': place[f'{prefix}_title'],
        'description': place[f'{prefix}_description'],
        'image': choice(images),
        'likes_count': randint(0, 30),
        'is_liked': bool(randint(0, 3)),
        'images_gallery': choices(images, k=4),
    }

    if type_ == 'locations':
        data['coords'] = parse_obj_as(Coordinates, place['object_coord'])
        return Block(type=type_, block=PlaceBlock(**data))  # time
    else:
        data['coords'] = Coordinates(lat=place['lat'], lon=place['lon'])

    return Block(
        type=type_,
        block=TourBlock(
            **data,
            price=f'{randint(1000, 7000)} руб',
            guide=choice(
                [
                    Guide(name='Vasiliy', avatar='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fphotos%2Fmen&psig=AOvVaw1-UAgPloYVYu9zvAUs4ewn&ust=1616992869566000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJjuof-V0u8CFQAAAAAdAAAAABAD'),
                    Guide(name='Peter', avatar='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fphotos%2Fone-young-man-only&psig=AOvVaw1-UAgPloYVYu9zvAUs4ewn&ust=1616992869566000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJjuof-V0u8CFQAAAAAdAAAAABAS'),
                    Guide(name='Misha', avatar='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pexels.com%2Fsearch%2Fman%2F&psig=AOvVaw1-UAgPloYVYu9zvAUs4ewn&ust=1616992869566000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJjuof-V0u8CFQAAAAAdAAAAABAX'),
                ]
            ),
            places=[],
        ),
    )


@api.post('/plan', response_model=Any, responses=responses)
def plan_trip(request: PlanRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    top_categories = [
        str(cat.id)
        for cat in sorted(request.categories, key=lambda category: category.weight, reverse=True)[
            :5
        ]
    ]
    region_id = get_region_by_name(db, request.city)
    days_count = (request.date_to - request.date_from).days + 1
    places_count = days_count * MAX_PLACES_PER_DAY

    tours = list(db.query(Tour).filter(Tour.c.local_id == region_id).limit(places_count))
    locations = list(
        db.query(Location)
        .filter(
            Location.c.type_id.op('?|')(array(top_categories)), Location.c.local_id == region_id
        )
        .limit(places_count)
    )
    joined = [*locations, *tours]
    shuffle(joined)
    places = joined[:places_count]

    days = defaultdict(list)
    for days_delta in range(days_count):
        cur_date = request.date_from + timedelta(days=days_delta)
        for _ in range(3):
            if len(places) == 0:
                break

            days[cur_date].append(places.pop(0))
        else:
            continue
        break

    result = []
    for day_date, places in days.items():
        blocks = [process_place(place) for place in places]
        for index, block in enumerate(blocks):
            block.time = datetime.combine(day_date, time(hour=9 + 3 * index))
        result.append(
            {'date': day_date, 'blocks': blocks}
        )

    return result

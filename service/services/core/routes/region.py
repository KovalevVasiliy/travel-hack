from typing import Any, Dict, List

from faker import Faker
from fastapi import Depends
from pymongo import MongoClient
from sqlalchemy.orm import Session

from crud import get_pop_region_categories, get_locations_by_region_name
from database import Category, Location
from services.api import responses
from services.dependencies import get_db

from . import api

images = [
        'https://www.pinterest.ru/pin/550846598154030932/',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fru.depositphotos.com%2Fstock-photos%2F%25D0%25B6%25D0%25B8%25D0%25B2%25D0%25BE%25D1%2582%25D0%25BD%25D1%258B%25D0%25B5.html&psig=AOvVaw0CnUGLQSVKMGAo1WhCJY6Q&ust=1616980487454000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMiokO7n0e8CFQAAAAAdAAAAABAI',
        'https://www.google.com/imgres?imgurl=https%3A%2F%2Fklike.net%2Fuploads%2Fposts%2F2019-03%2F1551512876_4.jpg&imgrefurl=https%3A%2F%2Fklike.net%2F1346-krasivye-kartinki-na-avu-50-foto.html&tbnid=W70yA3lZsaKgRM&vet=12ahUKEwjEuuPt59HvAhUFuioKHZyVCU0QMygbegUIARCvAQ..i&docid=aU-BdY9Ylbvz2M&w=650&h=650&q=rfhnbyrb&ved=2ahUKEwjEuuPt59HvAhUFuioKHZyVCU0QMygbegUIARCvAQ',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fbipbap.ru%2Fkrasivye-kartinki%2Fkrasivye-kartinki-na-rabochij-stol-vesna-35-foto.html&psig=AOvVaw0CnUGLQSVKMGAo1WhCJY6Q&ust=1616980487454000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMiokO7n0e8CFQAAAAAdAAAAABA4',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F841962092823189168%2F&psig=AOvVaw0CnUGLQSVKMGAo1WhCJY6Q&ust=1616980487454000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMiokO7n0e8CFQAAAAAdAAAAABA9',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fru.depositphotos.com%2Fstock-photos%2F%25D0%25B1%25D0%25B5%25D1%2581%25D0%25BF%25D0%25BB%25D0%25B0%25D1%2582%25D0%25BD%25D1%258B%25D0%25B5-%25D0%25BA%25D0%25B0%25D1%2580%25D1%2582%25D0%25B8%25D0%25BD%25D0%25BA%25D0%25B8.html&psig=AOvVaw0CnUGLQSVKMGAo1WhCJY6Q&ust=1616980487454000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMiokO7n0e8CFQAAAAAdAAAAABBD',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Ffotorelax.ru%2Fkrasivye-fotografii-i-kartinki-na-razlichnuyu-tematiku-2%2F&psig=AOvVaw0CnUGLQSVKMGAo1WhCJY6Q&ust=1616980487454000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMiokO7n0e8CFQAAAAAdAAAAABBJ',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fktonanovenkogo.ru%2Fvoprosy-i-otvety%2Fpriroda-chto-ehto-takoe.html&psig=AOvVaw0kMZURh8RB_oQALFMkXpTD&ust=1616980647121000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLjfzbro0e8CFQAAAAAdAAAAABAD',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fanngol.livejournal.com%2F198126.html&psig=AOvVaw0kMZURh8RB_oQALFMkXpTD&ust=1616980647121000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLjfzbro0e8CFQAAAAAdAAAAABAJ',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DC_1sjOg-VxY&psig=AOvVaw0kMZURh8RB_oQALFMkXpTD&ust=1616980647121000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLjfzbro0e8CFQAAAAAdAAAAABAU',
    ]


@api.get('/region/top-categories', response_model=List[Any], responses=responses)
def top_categories_by_region(city: str, db: Session = Depends(get_db)) -> List[Any]:
    return get_pop_region_categories(db, city)


@api.get('/region/locations', response_model=List[Any], responses=responses)
def locations_by_region_name(city: str, db: Session = Depends(get_db)) -> List[Any]:
    return get_locations_by_region_name(db, city)


@api.get('/generate/news', response_model=List[Dict[Any, Any]], responses=responses)
def generate_news(id: int, db: Session = Depends(get_db)) -> List[Dict[Any, Any]]:
    DB_URI = "mongodb://user:password@mongo:27017/travel-planner?authSource=admin"
    client = MongoClient(DB_URI)
    mongo = client['travel-planner']['collection']
    fake = Faker('ru_RU')
    likes = fake.random.randint(0, 10000)
    print('\n\n here')
    categories = [ent.id for ent in db.query(Category).all()]
    print(categories)
    locations = [ent.id for ent in db.query(Location).all()]
    print(locations)
    sources = ['google', 'facebook', 'tripadvizor', 'yahoo', 'yandex']

    for i in range(30):
        title = fake.text()[:15]
        description = fake.text()
        entity = {
            'title': title,
            'description': description,
            'preview': {
                'title': title,
                'description': description[:25],
                'category_id': fake.random.choice(categories),
                'source_name': fake.random.choice(sources),
                'image': fake.random.choice(images),
            },
            'social_info': {
                'likes': likes,
                'views': likes + fake.random.randint(0, 10000),
                'is_liked': False,
            },
            'content': [
                {'type': 'text', 'payload': fake.text()},
                {'type': 'image', 'payload': fake.random.choice(images)},
                {'type': 'location', 'payload': str(fake.random.choice(locations))},
            ],
            'id': i,
        }
        mongo.insert_one(entity)

    news = [news for news in mongo.find()]
    for n in news:
        print('first \n\n', n)
    return []

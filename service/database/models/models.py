from sqlalchemy import VARCHAR, Column, DefaultClause, ForeignKey, Integer, String, Table, Text
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, JSONB
from sqlalchemy.orm import relationship

from database import Base


class UserCategory(Base):
    __tablename__ = 'user_to_category'

    category_id = Column(Integer, ForeignKey('categories.category_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    rating = Column(Integer, nullable=False, default=1)
    user = relationship('user', back_populates='users')
    category = relationship('category', back_populates='categories')


UserNews = Table(
    'user_to_news',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('news_id', Integer, ForeignKey('news.news_id')),
)

UserLocation = Table(
    'user_to_locations',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('location_id', Integer, ForeignKey('gotorussia_travels_locations.id')),
)

UserTrip = Table(
    'user_to_trips',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('trip_id', Integer, ForeignKey('trips.trip_id')),
)


class Category(Base):
    __tablename__ = 'categories'

    id = Column('category_id', Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)


class News(Base):
    __tablename__ = 'news'
    id = Column('news_id', Integer, primary_key=True, index=True)


class Trip(Base):
    __tablename__ = 'trips'
    id = Column('trip_id', Integer, primary_key=True, index=True)


Location = Table(
    'gotorussia_travels_locations',
    Base.metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        nullable=False,
        server_default=DefaultClause("nextval('gotorussia_travels_locations_id_seq'::regclass)"),
        for_update=False,
    ),
    Column('object_title', String(255), nullable=False),
    Column('object_place', String(255)),
    Column('object_coord', String(255)),
    Column('object_description', Text, nullable=False),
    Column('adress', Text),
    Column('region_id', Integer),
    Column(
        'lat', DOUBLE_PRECISION(precision=53), server_default=DefaultClause('0'), for_update=False
    ),
    Column(
        'lon', DOUBLE_PRECISION(precision=53), server_default=DefaultClause('0'), for_update=False
    ),
)

Region = Table(
    'gotorussia_travels_regions',
    Base.metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        nullable=False,
        server_default=DefaultClause("nextval('gotorussia_travels_regions_id_seq'::regclass)"),
        for_update=False,
    ),
    Column('name', String(255), nullable=False),
    Column('region_id', Integer),
    Column('description', Text),
)


class User(Base):
    __tablename__ = 'users'

    id = Column('user_id', Integer, primary_key=True, index=True)
    fio = Column(String(100), nullable=False)
    avatar = Column(Text)

    categories = relationship('CategoryInterests', back_populates='user')
    news = relationship(News, secondary=UserNews)
    places = relationship(Location, secondary=UserLocation)
    trips = relationship(Trip, secondary=UserTrip)

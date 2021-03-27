from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, VARCHAR, DefaultClause
from sqlalchemy.dialects.postgresql import JSONB, DOUBLE_PRECISION
from sqlalchemy.orm import relationship

from database import Base


class UserCategory(Base):
    __tablename__ = 'user_to_category'

    category_id = Column(Integer, ForeignKey('categories.category_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    rating = Column(Integer, nullable=False, default=1)
    user = relationship('user', back_populates='users')
    category = relationship('category', back_populates='categories')


UserNews = Table('user_to_news', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('news_id', Integer, ForeignKey('news.news_id'))
)

#UserLocation = Table('user_to_locations', Base.metadata,
#    Column('user_id', Integer, ForeignKey('users.user_id')),
#    Column('location_id', Integer, ForeignKey('gotorussia_travels_locations.id'))
#)

UserTrip = Table('user_to_trips', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('trip_id', Integer, ForeignKey('trips.trip_id'))
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


location = Table(
    'gotorussia_travels_locations', Base.metadata,
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
    Column('lat', DOUBLE_PRECISION(precision=53), server_default=DefaultClause('0'), for_update=False),
    Column('lon', DOUBLE_PRECISION(precision=53), server_default=DefaultClause('0'), for_update=False),
)

"""
region = Table('gotorussia_travels_regions', MetaData(), Column('id', INTEGER(), table=<gotorussia_travels_regions>, primary_key=True, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f2ef88e0070>, for_update=False)), Column('orig_id', INTEGER(), table=<gotorussia_travels_regions>, nullable=False), Column('name', VARCHAR(length=255), table=<gotorussia_travels_regions>, nullable=False), Column('slug', VARCHAR(length=255), table=<gotorussia_travels_regions>, nullable=False), Column('created_at', TIMESTAMP(precision=0), table=<gotorussia_travels_regions>), Column('updated_at', TIMESTAMP(precision=0), table=<gotorussia_travels_regions>), Column('deleted_at', TIMESTAMP(precision=0), table=<gotorussia_travels_regions>), Column('territory_id', INTEGER(), table=<gotorussia_travels_regions>), Column('type_id', INTEGER(), table=<gotorussia_travels_regions>), Column('images', TEXT(), table=<gotorussia_travels_regions>), Column('region_id', INTEGER(), table=<gotorussia_travels_regions>), Column('geo', TEXT(), table=<gotorussia_travels_regions>), Column('local_id', INTEGER(), table=<gotorussia_travels_regions>), Column('intra_text', TEXT(), table=<gotorussia_travels_regions>), Column('description', TEXT(), table=<gotorussia_travels_regions>), Column('code', VARCHAR(length=255), table=<gotorussia_travels_regions>), Column('json_info', JSONB(astext_type=Text()), table=<gotorussia_travels_regions>), Column('points', JSON(astext_type=Text()), table=<gotorussia_travels_regions>), Column('short_desc', TEXT(), table=<gotorussia_travels_regions>), Column('map_points', JSON(astext_type=Text()), table=<gotorussia_travels_regions>), Column('important', BOOLEAN(), table=<gotorussia_travels_regions>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f2ef88e08e0>, for_update=False)), Column('kogo', VARCHAR(length=50), table=<gotorussia_travels_regions>), Column('komu', VARCHAR(length=50), table=<gotorussia_travels_regions>), Column('tk_id', INTEGER(), table=<gotorussia_travels_regions>), Column('phone', VARCHAR(length=20), table=<gotorussia_travels_regions>), Column('tpo_id', INTEGER(), table=<gotorussia_travels_regions>), Column('vinit', VARCHAR(length=50), table=<gotorussia_travels_regions>), Column('variations', JSONB(astext_type=Text()), table=<gotorussia_travels_regions>), schema=None)
"""


class User(Base):
    __tablename__ = 'users'

    id = Column('user_id', Integer, primary_key=True, index=True)
    fio = Column(String(100), nullable=False)
    avatar = Column(Text)

    categories = relationship('CategoryInterests', back_populates='user')
    news = relationship(News, secondary=UserNews)
    #places = relationship(Location, secondary=UserLocation)
    trips = relationship(Trip, secondary=UserTrip)

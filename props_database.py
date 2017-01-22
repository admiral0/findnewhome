from datetime import timedelta,datetime
from decimal import Decimal

from pony import orm

db = orm.Database()

def db_connect():
    db.bind('sqlite',"local.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)

class Property(db.Entity):
    ad_id = orm.PrimaryKey(int, auto=True)
    title = orm.Required(str)
    description = orm.Optional(orm.LongStr)
    price = orm.Required(Decimal)
    price_string = orm.Optional(str)
    main_photo = orm.Optional(str)
    address = orm.Required(str,unique=True)
    photos = set('Photo')
    position_longitude = orm.Required(Decimal, 20, 20)
    position_latitude = orm.Required(Decimal, 20, 20)
    bedrooms = orm.Required(int)
    bathrooms = orm.Optional(int)
    link = orm.Required(str)
    contact_email = orm.Optional(str)
    contact_phone = orm.Optional(str)
    by_bicycle = orm.Optional(timedelta)
    by_transit = orm.Optional(timedelta)
    by_transit_start = orm.Optional(datetime)
    distance_bicycle = orm.Optional(float)
    distance_transit = orm.Optional(float)
    transit_luas = orm.Optional(bool)
    transit_dart = orm.Optional(bool)
    hidden = orm.Required(bool, default=False)
    favorite = orm.Required(bool, default=False)

class Photo(db.Entity):
    photo_id = orm.PrimaryKey(int, auto=True)
    photo = orm.Required(str)
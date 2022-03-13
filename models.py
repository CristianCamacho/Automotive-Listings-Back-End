from email import charset
import os
from playhouse.db_url import connect
from enum import unique
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('listings.sqlite')

class Users(Model, UserMixin):
    username = CharField(unique=True)
    password = CharField(unique=True)
    class Meta:
        database = DATABASE

class Listings(Model):
    gov_vehicle_id = CharField()
    create_date = DateTimeField()
    year = CharField()
    make = CharField()
    model = CharField()
    fuel = CharField()
    city = CharField()
    highway = CharField()
    trans = CharField()
    cylinders = CharField()
    drive = CharField()
    mileage = CharField()
    zipcode = CharField()
    lien = BooleanField()
    vin = CharField()
    price = CharField()
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Listings, Users], safe=True)
    print('Tables Created')
    DATABASE.close()

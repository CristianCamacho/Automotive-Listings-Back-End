import os
from playhouse.db_url import connect
from enum import unique
from peewee import *

DATABASE = SqliteDatabase('listings.sqlite')

class Listings(Model):
    gov_vehicle_id = CharField()
    create_date = DateTimeField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Listings], safe=True)
    print('Tables Created')
    DATABASE.close()
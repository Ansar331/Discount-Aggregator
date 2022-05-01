import os
from peewee import *


PROJECT_PATH = os.getenv('PROJECT_PATH', '')
new_path = PROJECT_PATH + '/database/my_database.db'
db = SqliteDatabase(new_path)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Post(BaseModel):
    id = AutoField()
    title = CharField()
    description = CharField()
    discount = IntegerField()


class User(BaseModel):
    id = AutoField()
    name = CharField()
    email = CharField()
    password = CharField()

from peewee import *

db = SqliteDatabase('../../database/my_database.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Post(BaseModel):
    id = AutoField()
    title = CharField()
    description = CharField()
    discount = IntegerField()

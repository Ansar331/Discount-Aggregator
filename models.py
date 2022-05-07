import os
from peewee import *

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db_path ='/database/my_database.db'

db = SqliteDatabase(db_path)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel, UserMixin):
    id = AutoField()
    name = CharField()
    email = CharField()
    hashed_password = CharField()

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Post(BaseModel):
    id = AutoField()
    title = CharField()
    description = CharField()
    discount = IntegerField()
    title = CharField()
    user = ForeignKeyField(User, to_field='id')
    image_link = CharField()


models_list = [Post, User]


def setup_database():
    User.create_table()
    Post.create_table()

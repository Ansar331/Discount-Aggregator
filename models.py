import os
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash

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
    hashed_password = CharField()

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

models_list = [Post, User]

def create_tables():
    global models_list
    for model in model_list:
        model.create_table()


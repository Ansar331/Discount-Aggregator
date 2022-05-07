from playhouse.migrate import *
from models import User

my_db = SqliteDatabase('database/my_database.db')
migrator = SqliteMigrator(my_db)


def update_post_table():
    image_link = CharField(default='')
    image_link_update = migrator.add_column('post', 'image_link', image_link)

    migrate(image_link_update)


if __name__ == "__main__":
    update_post_table()
    print('migrations done')

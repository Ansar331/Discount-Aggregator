from .user import User


user = User()
User.create_table()


def create(title, discount, description):
    user = User(title=title, discount=discount, description=description)
    user.save()
    return user


def delete(user_id):
    user = User.select(User.id).where(User.id == user_id)
    user.delete_instance()


def update(user_id, discount, title, description):
    user = User.select(User.id).where(User.id == user_id)
    if title:
        user.title = title
    if discount:
        user.discount = discount
    if description:
        user.description = description
    user.save()

from models import Post
from models import User

post = Post()
Post.create_table()
user = User()
User.create_table()


def create_post(title, discount, description):
    post = Post(title=title, discount=discount, description=description)
    post.save()
    return post


def delete_post(post_id):
    post = Post.select(Post.id).where(Post.id == post_id)
    post.delete_instance()


def update_post(post_id, discount, title, description):
    post = Post.select(Post.id).where(Post.id == post_id)
    if title:
        post.title = title
    if discount:
        post.discount = discount
    if description:
        post.description = description
    post.save()


def create_user(name, email, password):
    user = User(name=name, email=email, password=password)
    user.save()
    return user


def delete_user(user_id):
    user = User.select(User.id).where(User.id == user_id)
    user.delete_instance()


def update_user(user_id, name, email, password):
    user = User.select(User.id).where(User.id == user_id)
    if name:
        user.name = name
    if email:
        user.email = email
    if password:
        user.password = password
    user.save()

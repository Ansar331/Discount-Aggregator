from .post import Post


post = Post()
Post.create_table()


def create(title, discount, description):
    post = Post(title=title, discount=discount, description=description)
    post.save()
    return post


def delete(post_id):
    post = Post.select(Post.id).where(Post.id == post_id)
    post.delete_instance()


def update(post_id, discount, title, description):
    post = Post.select(Post.id).where(Post.id == post_id)
    if title:
        post.title = title
    if discount:
        post.discount = discount
    if description:
        post.description = description
    post.save()

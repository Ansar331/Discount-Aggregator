#!flask/bin/python
import base64
import json
import datetime
from flask import g
from flask import Flask, request, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, session_protected
from werkzeug.utils import redirect


from models import User, Post

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    print('ok')
    return User.get(User.id == user_id)


@app.route('/create_post', methods=['POST'])
def createpost():
    title = request.form['title']
    description = request.form['description']
    discount = request.form['discount']
    post = post_services.create(title, discount, description)
    return {
        'post_id': post.id
    }


@app.route('/delete_post')
def deletepost():
    id = request.json['id']
    post_services.delete(id)
    return {'success': True}


@login_required
@app.route('/update_post/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.filter(Post.id == int(post_id)).first()
    if not post or post.user != current_user:
        return render_template('static/404.html')

    if request.method == 'GET':
        return render_template('static/edit_post.html', post=post)
    else:
        post.title = request.form['title']
        post.description = request.form['description']
        post.discount = request.form['discount']
        post.save()
        return redirect('/my_posts')

@login_required
@app.route('/delete_post/<post_id>')
def delete_post(post_id):
    post = Post.filter(Post.id==int(post_id)).first()
    if not post or post.user != current_user:
        return render_template('static/404.html')
    post.delete_instance()
    return redirect('/my_posts')


@app.route('/create_user', methods=['POST'])
def createuser():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    user = user_services.create(name, email, password)
    return {
        'user_id': user.id
    }


@app.route('/delete_user')
def deleteuser():
    id = request.json['id']
    user_services.delete(id)
    return {'success': True}


@app.route('/update_user')
def updateuser():
    id = request.json['id']
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    post = post_services.update(id, name, email, password)
    return {'success': True}


@login_required
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if not current_user.is_authenticated:
        return render_template('static/404.html')
    if request.method == 'GET':
        return render_template('static/post.html')
    else:
        post = Post.create(discount=request.form['discount'],
                           description=request.form['description'],
                           title=request.form['title'],
                           user=current_user)
        return redirect('')


@login_required
@app.route('/my_posts', methods=['GET', 'POST'])
def my_posts_page():
    my_posts = Post.select().where(Post.user==current_user)
    return render_template('static/my_posts.html', posts=my_posts)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    posts = Post.select()
    return render_template('static/main_page.html', posts=posts)


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('static/signin.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.select().where(User.email == email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            posts = Post.select()
            return render_template('static/main_page.html', user=user, posts=posts)
        return render_template('static/signin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/create_post_page')
def create_post_page():
    return render_template('static/post.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('static/signup.html')
    else:
        user = User.select().where(User.email == request.form['email']).first()
        if user:
            return render_template('static/signup.html', already_exists=True)
        else:
            user = User(email=request.form['email'],
                        name=request.form['first_name'])
            user.set_password(request.form['password'])
            user.save()
            return render_template('static/signin.html')


if __name__ == '__main__':
    app.run(debug=True)

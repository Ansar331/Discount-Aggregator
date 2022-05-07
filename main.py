#!flask/bin/python
import base64
import json
import datetime
import os
import smtplib

from flask import g, send_from_directory
from flask import Flask, request, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, session_protected
from werkzeug.utils import redirect

from config import EMAIL, EMAIL_PASSWORD
from models import User, Post

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'templates/media/'
app.config['ALLOWED_EXTENSIONS'] = ['jpg', 'png']
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 1000mb

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == user_id)


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
    post = Post.filter(Post.id == int(post_id)).first()
    if not post or post.user != current_user:
        return render_template('static/404.html')
    post.delete_instance()
    return redirect('/my_posts')


@app.route('/media/<path:filepath>', methods=['GET', 'POST'])
def media_share(filepath):
    print(filepath)
    return send_from_directory('', filepath)


@login_required
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'GET':
        return render_template('static/post.html')
    else:
        post_photo = request.files['photoFile']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], post_photo.filename)
        post_photo.save(file_path)

        post = Post.create(discount=request.form['discount'],
                           description=request.form['description'],
                           title=request.form['title'],
                           user=current_user,
                           image_link=file_path)
        return redirect('')


@login_required
@app.route('/my_posts', methods=['GET', 'POST'])
def my_posts_page():
    my_posts = Post.select().where(Post.user == current_user)
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


@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if request.method == 'GET':
        return render_template('static/feedback_form.html')
    else:
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            print(EMAIL, EMAIL_PASSWORD)
            smtp_server.login(EMAIL, EMAIL_PASSWORD)
            print(request.form['email'], request.form['message'])
            smtp_server.sendmail(request.form['email'], 'tiplar85@gmail.com', request.form['message'])
            smtp_server.close()
        except Exception as ex:
            print(ex)
            return redirect('static/404.html')
    return redirect('/feedback')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('static/signup.html')
    else:
        user = User.select().where(User.email == request.form['email']).first()
        if user:
            return render_template('static/signin.html', already_exists=True)
        else:
            user = User(email=request.form['email'],
                        name=request.form['first_name'])
            user.set_password(request.form['password'])
            user.save()
            return render_template('static/signin.html')


if __name__ == '__main__':
    app.run(debug=True)

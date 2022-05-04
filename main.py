#!flask/bin/python
import json
from flask import Flask, request, render_template
from models import User, Post

app = Flask(__name__)


@app.route('/create_post', methods=['POST'])
def createpost():
    print(request.form)
    title = request.form['title']
    description = request.form['description']
    discount = request.form['discount']
    post = post_services.create(description, discount, title)
    return {
        'post_id': post.id
    }


@app.route('/delete_post')
def deletepost():
    id = request.json['id']
    post_services.delete(id)
    return {'success': True}


@app.route('/update_post')
def updatepost():
    id = request.json['id']
    title = request.json['title']
    description = request.json['description']
    discount = request.json['discount']
    post = post_services.update(id, title, description, discount)
    return {'success': True}


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


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    return render_template('static/main_page.html')

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('static/signin.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.select().where(User.email==email).first()
        if user and user.check_password(password):
            posts = Post.select()
            return render_template('static/main_page.html', user=user, posts=posts)
        return render_template('static/signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('static/signup.html')
    else:
        user = User.select().where(User.email==request.form['email']).first()
        if user:
            return render_template('static/signup.html', already_exists=True)
        else:
            user = User(email=request.form['email'],
                        name=request.form['first_name'])
            user.set_password(request.form['password'])
            user.save()
            return render_template('static/signin.html')


@app.route('/create_post_page')
def create_post_page():
    return render_template('static/post.html')


if __name__ == '__main__':
    app.run(debug=True)

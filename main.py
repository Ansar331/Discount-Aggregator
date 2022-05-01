#!flask/bin/python
from flask import Flask, request, render_template
from models.post import post_services
from models.user import user_services
import json


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


@app.route('/login_page')
def login_page():
    return render_template('static/signin.html')


@app.route('/create_post_page')
def create_post_page():
    return render_template('static/post.html')


if __name__ == '__main__':
    app.run(debug=True)

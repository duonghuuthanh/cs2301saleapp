from flask import render_template, request, redirect
from flask_login import login_user, logout_user
from eapp import app, dao, login
import math


@app.route('/')
def index():
    return render_template('index.html',
                           pages=math.ceil(dao.count_products()/app.config['PAGE_SIZE']),
                           products=dao.get_products(category_id=request.args.get('category_id'),
                                                     kw=request.args.get('kw'),
                                                     page=request.args.get('page', 1)))


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.route('/register')
def register_view():
    return render_template('register.html')


@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    next = request.args.get('next')
    return redirect(next if next else '/')


@login.user_loader
def load_user(pk):
    return dao.get_user_by_id(pk)


@app.context_processor
def common_responses():
    return {
        'categories': dao.get_categories()
    }


if __name__ == '__main__':
    from eapp import admin
    app.run(debug=True)

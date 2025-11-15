from flask import render_template, request, redirect
from eapp import app, dao, login
from flask_login import login_user, logout_user
import math


@app.route('/')
def index():
    products = dao.load_products(cate_id=request.args.get('category_id'),
                                 kw=request.args.get('kw'),
                                 page=int(request.args.get('page', 1)))

    return render_template('index.html', products=products,
                           pages=math.ceil(dao.count_products()/app.config['PAGE_SIZE']))


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')


@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    next = request.args.get('next')
    return redirect(next if next else '/admin')


@app.context_processor
def common_responses():
    return {
        'categories': dao.load_categories()
    }

@login.user_loader
def load_user(id):
    return dao.get_user_by_id(id)


if __name__ == '__main__':
    from eapp import admin
    app.run(debug=True)

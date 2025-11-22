from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user, logout_user
from eapp import app, dao, login, utils
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


@app.route('/register', methods=['post'])
def register_process():
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if password != confirm:
        err_msg = 'Mật khẩu KHÔNG khớp'
        return render_template('register.html', err_msg=err_msg)

    avatar = request.files.get('avatar')
    try:
        dao.add_user(avatar=avatar,
                    name=request.form.get('name'),
                    username=request.form.get('username'),
                    password=request.form.get('password'))
    except Exception as ex:
        return render_template('register.html', err_msg="Hệ thống đang có lỗi!")

    return redirect('/login')


@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    next = request.args.get('next')
    return redirect(next if next else '/')


@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@app.route('/api/carts/<int:id>', methods=['put'])
def update_to_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        quantity = int(request.json['quantity'])
        cart[id]['quantity'] = quantity

    session['cart'] = cart
    return jsonify(utils.count_carts(cart))


@app.route('/api/carts/<int:id>', methods=['delete'])
def delete_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        del cart['id']

    session['cart'] = cart
    return jsonify(utils.count_carts(cart))

@app.route('/api/carts', methods=['post'])
def add_to_cart():
    data = request.json

    cart = session.get('cart')
    if not cart:
        cart = {}

    id, name, price = str(data.get('id')), data.get('name'), data.get('price')

    if id in cart:
        cart[id]["quantity"] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    """
        {
            "1": {
                "id": 1,
                "name": "...",
                "price": 99,
                "quantity": 2
            }, "2": {
                "id": 2,
                "name": "...",
                "price": 99,
                "quantity":5
            }
        }
    """
    return jsonify(utils.count_carts(cart))

@app.route('/cart')
def cart_view():
    return render_template('cart.html')

@login.user_loader
def load_user(pk):
    return dao.get_user_by_id(pk)


@app.context_processor
def common_responses():
    return {
        'categories': dao.get_categories(),
        'cart_stats': utils.count_carts(session.get('cart'))
    }


if __name__ == '__main__':
    from eapp import admin
    app.run(debug=True)

#!/usr/bin/env python
'''
    wechat business helper

    How to put SQLAlchemy models in a seperate file
    https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
'''

import datetime
from functools import wraps
import json

from flask import Flask, render_template, redirect, url_for, jsonify, request, make_response
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid

from config import config
from tracking import Tracking
from models import db, Order, User

app = Flask(__name__)
Bootstrap(app)
app.config.update(config)

mysql = MySQL(app)
db.init_app(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


###
#   Forms
###

class ShowMyOrderForm(FlaskForm):
    client = StringField('收件人', validators=[DataRequired()])
    phone = StringField('电话', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShowMyOrderForm()
    if form.validate_on_submit():
        return redirect(
            url_for('orders', client=form.client.data, phone=form.phone.data)
        )
    else:
        return render_template('index.html', form=form)


@app.route('/orders/<client>/<phone>')
def orders(client, phone):
    cur = mysql.connection.cursor()

    if (client == 'lucaslinus') and (phone == 'linuslucas'):
        query = '''
        SELECT
            client,
            tracking,
            carrier,
            product,
            price,
            quantity,
            DATE(created_time) AS created_time
        FROM usatocn2013.orders
        ORDER BY created_time DESC;
        '''
    else:
        query = '''
        SELECT
            client,
            tracking,
            carrier,
            product,
            price,
            quantity,
            DATE(created_time) AS created_time
        FROM usatocn2013.orders
        WHERE client = '{client}'
        AND phone = '{phone}'
        ORDER BY created_time DESC;
        '''.format(client=client, phone=phone)

    cur.execute(query)
    orders = cur.fetchall()

    if not orders:
        return render_template(
            'no_order_found.html', client=client, phone=phone)
    else:
        return render_template('orders.html', orders=orders)


@app.route('/orders/tracking_status/<tracking_number>/<carrier>')
def tracking_status(tracking_number, carrier):
    tracking_obj = Tracking.get_tracking_object(tracking_number, carrier)
    statuses = tracking_obj.track()

    return render_template('tracking_status.html', statuses=statuses)

###
# API
###

###
#   Authentication API
###


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'code': 50008, 'data': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/user/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    username = auth['username']
    password = auth['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, password):
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
            app.config['SECRET_KEY']
        )

        return jsonify({
            "code": 20000,
            "data": {
                "token": token.decode('UTF-8')
            }
        })

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/api/user/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({
        "code": 20000,
        "data": "success"
    })


@app.route('/api/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {
            'username': user.username,
            'password': user.password,
            'admin': user.admin,
        }
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/api/user/<username>', methods=['GET'])
@token_required
def get_one_user(current_user, username):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {
        'username': user.username,
        'password': user.password,
        'admin': user.admin,
    }

    return jsonify({'user': user_data})


@app.route('/api/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()

    username = data['username']
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists.'})

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        username=username, password=hashed_password, admin=False
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/api/user/<username>', methods=['PUT'])
@token_required
def promote_user(current_user, username):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@app.route('/api/user/<username>', methods=['DELETE'])
@token_required
def delete_user(current_user, username):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


@app.route('/api/user/info', methods=['GET'])
@token_required
def get_user_info(current_user):

    role = 'admin' if current_user.admin else 'worker'
    response = {
        "code": 20000,
        "data": {
            "role": [
                role
            ],
            "name": current_user.username,
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
        }
    }

    return jsonify(response)


@app.route('/api/order', methods=['GET'])
@token_required
def get_all_orders(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    # date_range = json.loads(request.args.get('dateRange'))
    # if date_range:
    #     date_start, _, date_end = date_range.split('-')

    date_range = None

    query = json.loads(request.args.get('search'))
    if query.get('value'):
        query_value = '%{}%'.format(query['value'])
        query_key = query['key']

    show_no_tracking = json.loads(request.args.get('showNoTracking'))

    if query.get('value') and show_no_tracking:
        orders = Order.query.filter(
            getattr(Order, query_key).like(query_value),
            Order.tracking == ''
        ).order_by(Order.created_time.desc()).all()
    elif query.get('value') and not show_no_tracking:
        orders = Order.query.filter(
            getattr(Order, query_key).like(query_value)
        ).order_by(Order.created_time.desc()).all()
    elif show_no_tracking and not query.get('value'):
        orders = Order.query.filter(
            Order.tracking == ''
        ).order_by(Order.created_time.desc()).all()
    else:
        orders = Order.query.order_by(Order.created_time.desc()).all()

    output = []
    for order in orders:
        new = {
            'order_id': str(order.order_id),
            'client': order.client,
            'phone': order.phone,
            'product': order.product,
            'price': str(int(order.price)),
            'cost': str(int(order.cost)),
            'quantity': str(order.quantity),
            'tracking': order.tracking,
            'carrier': order.carrier,
            'created_time': order.created_time,
        }
        output.append(new)

    return jsonify({
        'code': 20000,
        'data': {
            'orders': output
        }
    })


@app.route('/api/order', methods=['POST'])
@token_required
def create_order(current_user):
    print('Creating Order')
    if not current_user.admin:
        return jsonify({'code': 20001, 'data': 'Cannot perform that function!'})

    data = request.get_json()

    new_order = Order(
        client=data['client'],
        phone=data['phone'],
        product=data['product'],
        price=data['price'],
        cost=data.get('cost'),
        quantity=data['quantity'],
        tracking=data.get('tracking', ''),
        carrier=data.get('carrier', ''),
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'code': 20000, 'data': "Order created!"})


@app.route('/api/order/<order_id>', methods=['PUT'])
@token_required
def update_order(current_user, order_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    order = Order.query.filter_by(order_id=order_id).first()

    if not order:
        return jsonify({'message': 'No order found!'})

    data = request.get_json()
    print(data)
    for key, value in data.items():
        setattr(order, key, value)

    db.session.commit()

    return jsonify({'code': 20000, 'data': 'Order record has been updated!'})


@app.route('/api/order/<order_id>', methods=['DELETE'])
@token_required
def delete_order(current_user, order_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    order = Order.query.filter_by(order_id=order_id).first()

    if not order:
        return jsonify({'code': 20001, 'data': 'No order found!'})

    db.session.delete(order)
    db.session.commit()

    return jsonify({'code': 20000, 'data': 'Order record deleted!'})

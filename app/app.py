#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
    wechat business helper

    How to put SQLAlchemy models in a seperate file
    https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045

    3/31/2018   Hide tracking button when no tracking number available
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
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid

from config import config
import sql
from tracking import tracking_shipment
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

    query = '''
    SELECT
        client,
        tracking,
        carrier,
        forward_tracking,
        forward_carrier,
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
    cur.close()

    if not orders:
        return render_template(
            'no_order_found.html', client=client, phone=phone)
    else:
        return render_template('orders.html', orders=orders)


@app.route(
    '/orders/tracking_status/<tracking_number>/<carrier>',
    defaults={'forward_tracking': None, 'forward_carrier': None}
)
@app.route('/orders/tracking_status/<tracking_number>/<carrier>/<forward_tracking>/<forward_carrier>')
def tracking_status(tracking_number, carrier, forward_tracking, forward_carrier):

    statuses = tracking_shipment(tracking_number, carrier)

    if forward_tracking and forward_carrier:
        forward_statuses = tracking_shipment(forward_tracking, forward_carrier)
        statuses = forward_statuses + statuses

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
            return jsonify({'code': 50014, 'data': 'Token is missing!'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'code': 50014, 'data': 'Token is invalid!'})

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/user/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="No Password"'})

    username = auth['username']
    password = auth['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="No Username"'})

    if check_password_hash(user.password, password):
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)},
            app.config['SECRET_KEY']
        )

        return jsonify({
            "code": 20000,
            "data": {
                "token": token.decode('UTF-8'),
                "userId": user.user_id
            }
        })

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Wrong Auth Info"'})


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

    search = json.loads(request.args.get('search'))
    page = int(request.args.get('page'))
    per_page = int(request.args.get('limit'))

    search_value = search.get('value')

    if search_value:
        search_value_like = '%{}%'.format(search['value'])
        search_key = search['key']

    show_no_tracking = json.loads(request.args.get('showNoTracking'))

    if search_value and show_no_tracking:
        cursor = Order.query.filter(
            getattr(Order, search_key).like(search_value_like),
            Order.tracking == ''
        ).order_by(
            Order.created_time.desc()
        )
    elif search_value and not show_no_tracking:
        cursor = Order.query.filter(
            getattr(Order, search_key).like(search_value_like)
        ).order_by(
            Order.created_time.desc()
        )
    elif show_no_tracking and not search_value:
        cursor = Order.query.filter(
            Order.tracking == ''
        ).order_by(
            Order.created_time.desc()
        )
    else:
        cursor = Order.query.filter(
            Order.client != '张三'
        ).order_by(
            Order.created_time.desc()
        )

    total = cursor.count()
    orders = cursor.paginate(page, per_page, False).items

    output = []
    for order in orders:
        new = {
            'order_id': order.order_id,
            'client': order.client,
            'phone': order.phone,
            'product': order.product,
            'price': str(int(order.price)),
            'cost': str(int(order.cost)),
            'shipping': order.shipping,
            'quantity': str(order.quantity),
            'tracking': order.tracking,
            'carrier': order.carrier,
            'forward_tracking': order.forward_tracking,
            'forward_carrier': order.forward_carrier,
            'created_time': order.created_time,
        }
        output.append(new)

    return jsonify({
        'code': 20000,
        'data': {
            'orders': output,
            'total': total
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
        order_id=data['order_id'],
        client=data['client'],
        phone=data['phone'],
        product=data['product'],
        price=data['price'],
        cost=data.get('cost'),
        shipping=data['shipping'],
        quantity=data['quantity'],
        tracking=data.get('tracking', ''),
        forward_tracking=data.get('forward_tracking', ''),
        carrier=data.get('carrier', ''),
        forward_carrier=data.get('forward_carrier', ''),
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


@app.route('/api/tracking', methods=['POST'])
@token_required
def get_tracking_status(current_user):
    data = request.get_json()
    try:
        statuses = tracking_shipment(data['tracking_number'], data['carrier'])
    except Exception:
        statuses = {'time': '', 'status': '出错啦，无法获取物流状态。'}

    return jsonify({'code': 20000, 'data': {'statuses': statuses}})


###
#   Sales Statistics
###

@app.route('/api/stats/monthly_sales', methods=['GET'])
@token_required
def get_monthly_sales_stats(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})
    query = sql.GET_MONTHLY_SALES
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return jsonify({'code': 20000, 'data': data})


@app.route('/api/stats/monthly_sales/count_to', methods=['GET'])
@token_required
def get_monthly_sales_count_to(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})
    query = sql.GET_THIS_MONTH_COUNT_TO
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchone()
    cur.close()

    if not data:
        data = {
            'sales': 0,
            'gross_profit': 0,
            'year': datetime.datetime.utcnow().year,
            'month': datetime.datetime.utcnow().month,
        }

    return jsonify({'code': 20000, 'data': data})


@app.route('/api/stats/client_ranking/alltime', methods=['GET'])
@token_required
def get_alltime_client_ranking_stats(current_user):
    query = sql.GET_ALLTIME_CLIENT_RANKING
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return jsonify({'code': 20000, 'data': data})


@app.route(
    '/api/stats/client_ranking/<start_date>/<end_date>',
    methods=['GET']
)
@token_required
def get_period_client_ranking_stats(current_user, start_date, end_date):
    query = sql.GET_PERIOD_CLIENT_RANKING.format(
        start_date=start_date, end_date=end_date
    )
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return jsonify({'code': 20000, 'data': data})


@app.route('/api/stats/daily_sales', methods=['GET'])
@token_required
def get_daily_sales_summary(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})
    query = sql.GET_DAILY_SALES_SUMMARY
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    db_output = {str(item['date']): item for item in data}

    base = datetime.datetime.today()
    numdays = base.day
    date_list = [
        str((base - datetime.timedelta(days=x)).date())
        for x in range(0, numdays)
    ][::-1]

    sales = []
    gross_profit = []
    dates = []
    for date in date_list:
        if date in db_output:
            dates.append(date)
            sales.append(db_output[date]['sales'])
            gross_profit.append(db_output[date]['gross_profit'])
        else:
            dates.append(date)
            sales.append(0)
            gross_profit.append(0)

    result = {
        'date': dates,
        'sales': sales,
        'gross_profit': gross_profit
    }

    return jsonify({'code': 20000, 'data': result})

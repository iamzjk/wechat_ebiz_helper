#!/usr/bin/env python
'''
    wechat business helper
'''

from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_cors import CORS

from config import config
from tracking import Tracking

app = Flask(__name__)
Bootstrap(app)
app.config.update(config)
mysql = MySQL(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


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
        FROM usatocn2013.orders;
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
        AND phone = '{phone}';
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


@app.route('/api/orders/<client>/<phone>')
def get_my_orders(client, phone):
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
        FROM usatocn2013.orders;
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
        AND phone = '{phone}';
        '''.format(client=client, phone=phone)

    cur.execute(query)
    orders = cur.fetchall()

    if not orders:
        return jsonify({'data': 'no order found'})
    else:
        return jsonify({'data': orders})


@app.route('/api/tracking/<tracking_number>/<carrier>')
def get_tracking_status(tracking_number, carrier):
    tracking_obj = Tracking.get_tracking_object(tracking_number, carrier)
    statuses = tracking_obj.track()

    return jsonify({'data': statuses})


@app.route('/api/orders/new/', methods=['POST'])
def add_one_new_order():
    new_order = request.json['order']
    _insert_one_order(new_order)

    return jsonify({'data': {'order': new_order, 'status': 'inserted'}})


def _insert_one_order(order):
    query = '''
    INSERT INTO usatocn2013.orders(client, phone, product, price, cost, quantity, tracking, carrier)
    VALUES("{client}", "{phone}", "{product}", {price}, {cost}, {quantity}, "{tracking}", "{carrier}")
    '''.format(**order)

    con = mysql.connection
    cur = con.cursor()
    cur.execute(query)
    con.commit()

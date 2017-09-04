#!/usr/bin/env python
'''
    wechat business helper v0.1.0
'''

from flask import Flask, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from tracking import Tracking

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'usatocn2013'
app.config['JSON_AS_ASCII'] = False
app.config['MYSQL_HOST'] = 'iamzjk.mynetgear.com'
app.config['MYSQL_USER'] = 'jelfsony'
app.config['MYSQL_PASSWORD'] = 'jelfsony0910'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


class ShowMyOrderForm(FlaskForm):
    client = StringField('姓名', validators=[DataRequired()])
    phone = StringField('电话', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShowMyOrderForm()
    if form.validate_on_submit():
        return redirect(url_for('orders', client=form.client.data, phone=form.phone.data))
    else:
        return render_template('index.html', form=form)


@app.route('/orders/<client>/<phone>')
def orders(client, phone):
    cur = mysql.connection.cursor()

    query = '''
    SELECT
        client,
        tracking,
        product,
        price,
        quantity,
        DATE(created_time) AS created_time
    FROM usatocn2013.orders
    WHERE client = '{client}'
    AND phone = '{phone}'
    '''.format(client=client, phone=phone)

    cur.execute(query)
    orders = cur.fetchall()

    return render_template('orders.html', orders=orders)


@app.route('/orders/tracking_status/<tracking_number>')
def tracking_status(tracking_number):

    tracking = Tracking(tracking_number)
    statuses = tracking.run()

    return render_template('tracking_status.html', statuses=statuses)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

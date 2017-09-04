#!/usr/bin/env python
'''
    wechat business helper
'''

from flask import Flask, jsonify, render_template
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
app.config['JSON_AS_ASCII'] = False
app.config['MYSQL_HOST'] = 'iamzjk.mynetgear.com'
app.config['MYSQL_USER'] = 'jelfsony'
app.config['MYSQL_PASSWORD'] = 'jelfsony0910'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def index():
    # return '橙昕美购 - 订单与快递查询系统<br>微信：jelfsony'
    return render_template('index.html')


@app.route('/orders/<client>/<phone>')
def orders(client, phone):
    cur = mysql.connection.cursor()

    query = '''
    SELECT
        order_id,
        client,
        phone,
        product,
        price,
        quantity,
        tracking,
        DATE(created_time) AS created_time
    FROM usatocn2013.orders
    WHERE client = '{client}'
    AND phone = '{phone}'
    '''.format(client=client, phone=phone)

    cur.execute(query)
    orders = cur.fetchall()
    # orders = jsonify(orders)

    return render_template('orders.html', orders=orders)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

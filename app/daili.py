#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
    This route is for agents. It hides all price and upstream info,
    so agent can provide it to their customers
'''

from flask import Blueprint, redirect, url_for, render_template

from models import Order
from forms import ShowMyOrderForm
from tracking import tracking_shipment

daili = Blueprint('daili', __name__)


@daili.route('/', methods=['GET', 'POST'])
def index():
    form = ShowMyOrderForm()
    if form.validate_on_submit():
        return redirect(
            url_for(
                '.orders',
                client=form.client.data.strip(),
                phone=form.phone.data.strip()
            )
        )
    else:
        return render_template('daili/index.html', form=form)


@daili.route('/orders/<client>/<phone>')
def orders(client, phone):
    '''
        Orders of a specific client
    '''
    orders = Order.query.filter_by(client=client, phone=phone).all()

    if not orders:
        return render_template(
            'daili/no_order_found.html', client=client, phone=phone)
    else:
        return render_template('daili/orders.html', orders=orders)


@daili.route(
    '/orders/tracking_status/<tracking_number>/<carrier>',
    defaults={'forward_tracking': None, 'forward_carrier': None}
)
@daili.route(
    '/orders/tracking_status/<tracking_number>/'
    '<carrier>/<forward_tracking>/<forward_carrier>'
)
def tracking_status(
    tracking_number, carrier, forward_tracking, forward_carrier
):

    statuses = tracking_shipment(tracking_number, carrier)

    if forward_tracking and forward_carrier:
        forward_statuses = tracking_shipment(forward_tracking, forward_carrier)
        statuses = forward_statuses + statuses

    return render_template('daili/tracking_status.html', statuses=statuses)

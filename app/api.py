#!/usr/bin/env python
'''
    API
'''

# from flask import Blueprint, render_template, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# api = Blueprint('api', __name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)

#     def __init__(self, username, email):
#         self.username = username
#         self.email = email

#     def __repr__(self):
#         return '<User %r>' % self.username






# @api.route('/', methods=['GET', 'POST'])
# def get_my_orders():
#     form = ShowMyOrderForm()
#     if form.validate_on_submit():
#         return redirect(
#             url_for('orders', client=form.client.data, phone=form.phone.data)
#         )
#     else:
#         return render_template('index.html', form=form)

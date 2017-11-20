# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, String, text
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    client = Column(String(25, 'utf8_unicode_ci'), nullable=False)
    phone = Column(String(15, 'utf8_unicode_ci'), nullable=False)
    product = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    price = Column(Float(10, True), nullable=False)
    cost = Column(Float(10, True), nullable=False)
    shipping = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    tax_pct = Column(Float(10, True), nullable=False, server_default=text("'0.00'"))
    tracking = Column(String(50, 'utf8_unicode_ci'), server_default=text("''"))
    carrier = Column(String(15, 'utf8_unicode_ci'), server_default=text("''"))
    created_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_time = Column(DateTime)


class User(db.Model):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(80))
    admin = Column(Integer)
    comment = Column(String(50))

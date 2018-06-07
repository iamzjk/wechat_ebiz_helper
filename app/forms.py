'''
    Forms
'''

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ShowMyOrderForm(FlaskForm):
    client = StringField('收件人', validators=[DataRequired()])
    phone = StringField('电话', validators=[DataRequired()])

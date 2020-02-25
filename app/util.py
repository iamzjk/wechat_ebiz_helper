'''
    Util Functions
'''

from decimal import Decimal
import requests


def sqlalchemy_to_dict(object):
    '''
        convert db.engine.execute() output to dict
    '''

    rows = object.fetchall()
    converted_rows = []

    for row in rows:
        new_row = []
        for value in row:
            if isinstance(value, Decimal):
                new_row.append(float(value))
            else:
                new_row.append(value)
        converted_rows.append(new_row)

    return [dict(zip(object.keys(), row)) for row in converted_rows]


def exchange_rate(base, target):
    """
        exchange_rate from base to target currency
        example:
            exchange_rate('USD', 'CNY')
    """
    url = 'https://api.exchangeratesapi.io/latest?base={}&symbols={}'.format(base, target)
    resp = requests.get(url)
    # response format
    # {"rates":{"CNY":7.0347568867},"base":"USD","date":"2020-02-24"}

    data = resp.json()
    return {
        'rate': data['rates'][target],
        'date': data['date']
    }

'''
    Util Functions
'''

from decimal import Decimal

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

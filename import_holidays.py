from __future__ import unicode_literals
import csv, datetime

from FinanceDBAPI import FinanceDB

def import_holiday_type(filename, db):
    with open(filename) as f:
        types = list(csv.reader(f))
    for k, v in enumerate(types):
        if k == 0:
            continue
        item = db.Holiday_type(type_id = v[0], type_name = v[1])

        db.add(item)
    try:
        db.commit()
    except Exception as e:
        print(e)

def import_holidays(filename, db):
    with open(filename) as f:
        holidays = list(csv.reader(f))

    for k, v in enumerate(holidays):
        if k == 0:
            continue
        item = db.Holidays(holiday_date=datetime.datetime.strptime(v[0],
            "%Y%m%d").date(), holiday_type_id = int(v[1]))
        db.add(item)
    try:
        db.commit()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    
    db = FinanceDB()
    import_holiday_type('holiday_type.csv', db)
    import_holidays('holidays.csv', db)

import datetime

end_date = datetime.datetime.utcnow()
start_date = end_date - datetime.timedelta(days=8)
difference_in_days = abs((end_date - start_date).days)
print(end_date)
print(difference_in_days)
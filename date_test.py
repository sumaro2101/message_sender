import datetime 



result_1 = datetime.timedelta(days=40)
result_2 = datetime.datetime(year=2024, month=7, day=18, hour=10, minute=30, second=10) - datetime.datetime.now()
result_3 = result_1.total_seconds() - result_2.total_seconds()
print(result_2)
print(result_3)
print(result_1.total_seconds())
print((result_3 / result_1.total_seconds()) * 100)

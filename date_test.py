import datetime 



result_1 = datetime.timedelta(days=40)
result_2 = datetime.datetime(year=2024, month=7, day=18, hour=10, minute=30, second=10) - datetime.datetime.now()
result_3 = result_1.total_seconds() - result_2.total_seconds()
print(result_2)
print(result_3)
print(result_1.total_seconds())
print((result_3 / result_1.total_seconds()) * 100)

pk = 'mail_center.sendingmessage_65'.split('_')[-1]
print(pk)

def test_2(*args, **kwargs):
    print(kwargs)

def test_1(*args, **kwargs):
    name = 'name'
    kwargs.update(**{'object_unique_name': name})
    test_2(**kwargs)
    
    
kwargs = {'email_template_name': 'mail_form/mail_send_form.html'}
test_1(**kwargs)

url = 'fafasfsa/fsaf/?fdsf=sfd'

print(url[::-1].replace('/', '', 1)[::-1])
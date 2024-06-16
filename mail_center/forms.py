from django.forms import fields, forms, ModelForm, DateTimeInput
from formset.widgets import DateTimePicker, DateTimeInput
from mail_center.models import SendingMessage
from datetime import timedelta


class FormSendMesssage(ModelForm):
    date_first_send = fields.DateTimeField(widget=DateTimeInput, required=False)
    
    class Meta:
        model = SendingMessage
        fields = ('clients', 'periodicity', 'date_first_send')
        
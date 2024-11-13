from django.forms import fields, ModelForm
from django.db.models import Q

from formset.widgets import DateTimeInput as FormSetDataTimeInput

from datetime import datetime, timezone, timedelta

from mail_center.models import SendingMessage


class FormSendMesssage(ModelForm):

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.user = kwargs.pop('user')
        else:
            self.user = None
        super().__init__(*args, **kwargs)

    date_first_send = fields.DateTimeField(
        widget=FormSetDataTimeInput(
            attrs={'class': 'form-control form-control-sm'},
            ),
        required=False,
        label='Начало отправки',
        )

    def get_initial_for_field(self, field, field_name: str):
        """Здесь реализованно изменение вывода поля клиентов
        в зависимости от пользователя
        """
        if not self.user.is_staff and not self.user.is_superuser:
            self.fields['clients'].queryset = (self.fields['clients']
                                               .queryset
                                               .filter(Q(employee=self.user,
                                                         actual=True))
                                               .order_by(
                                                   'client_first_name',
                                                   ))
        else:
            self.fields['clients'].queryset = (self.fields['clients']
                                               .queryset
                                               .order_by('-actual',
                                                         'client_first_name',
                                                         ))
        return super().get_initial_for_field(field, field_name)

    def clean_date_first_send(self):
        date_first_send = self.cleaned_data.get('date_first_send')
        if date_first_send:
            if (date_first_send <
                datetime.now(timezone.utc) - timedelta(seconds=30)):
                self.add_error(
                    'date_first_send',
                    'Время не может быть задним числом',
                    )
        return date_first_send

    class Meta:
        model = SendingMessage
        fields = ('clients', 'periodicity', 'date_first_send')

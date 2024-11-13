from django import forms
from .models import ClientServise


class AddClientForm(forms.ModelForm):

    class Meta:
        model = ClientServise
        fields = ('client_mail',
                  'client_first_name',
                  'client_last_name',
                  'client_middle_name',
                  'client_info',
                  )

from django import forms
from .models import MessageInfo


class CreateMessageForm(forms.ModelForm):

    class Meta:
        model = MessageInfo
        fields = ['title_message', 'text_message',]
        widgets = {
            'title_message': forms.TextInput(),
            'text_message': forms.Textarea(),
        }

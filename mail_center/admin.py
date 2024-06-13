from django.contrib import admin
from .models import SendingMessage

# Register your models here.

@admin.register(SendingMessage)
class SendingMessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'message', 'date_first_send', 'periodicity', 'status']
    

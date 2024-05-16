from django.contrib import admin
from .models import ClientServise

# Register your models here.

@admin.register(ClientServise)
class ClientServiseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'employee', 'client_mail', 'client_first_name', 'client_last_name', 'client_middle_name', 'client_info', 'time_create', 'time_edit', 'actual']
    list_filter = ('actual',)
    search_fields = ('employee', 'time_create', 'time_edit', 'client_mail', 'client_first_name', 'client_last_name', 'client_middle_name')
    
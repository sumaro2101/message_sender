from django.contrib import admin
from .models import MessageInfo
# Register your models here.


@admin.register(MessageInfo)
class MessageInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'employee', 'title_message', 'text_message', 'slug', 'time_create', 'time_edit', 'actual']
    list_filter = ('actual',)
    search_fields = ('time_create', 'time_edit', 'title_message')
    
    prepopulated_fields = {'slug': ('employee', 'title_message')}

# Register your models here.

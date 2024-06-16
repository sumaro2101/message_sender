from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

    
@admin.register(User)
class PostCommentAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name', 'password')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest

from .models import User

    
@admin.register(User)
class PostCommentAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request).exclude(Q(is_staff=True) | Q(is_superuser=True))
        return queryset
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        if not request.user.is_superuser or request.user.groups.filter(name='moderator').exists():
            self.readonly_fields = ('username',
                                    'email',
                                    'first_name',
                                    'last_name',
                                    'password',
                                    'is_staff',
                                    'is_superuser',
                                    'groups',
                                    'user_permissions',
                                    'date_joined',
                                    'last_login',
                                    )
            
        return super().get_readonly_fields(request, obj)
    
from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class PostCommentAdmin(UserAdmin):
    list_display = ('pk',
                    'username',
                    'email',
                    'is_verify_email',
                    'first_name',
                    'last_name',
                    'password',
                    'is_staff',
                    'is_superuser',
                    'is_active',
                    'date_joined',
                    'last_login',
                    )
    search_fields = ('username', 'first_name', 'last_name', 'email')

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name",
                                         "last_name",
                                         "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_verify_email",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if not request.user.is_superuser:
            queryset = super().get_queryset(request)
            queryset = queryset.exclude(Q(is_staff=True) |
                                        Q(is_superuser=True))
        else:
            queryset = super().get_queryset(request)
        return queryset

    def get_readonly_fields(self,
                            request: HttpRequest,
                            obj: Any | None = ...) -> (list[str] |
                                                       tuple[Any, ...]):
        if (not request.user.is_superuser
            or request.user.groups.filter(name='moderator').exists()):
            self.readonly_fields = ['username',
                                    'email',
                                    'is_verify_email',
                                    'first_name',
                                    'last_name',
                                    'password',
                                    'is_staff',
                                    'is_superuser',
                                    'groups',
                                    'user_permissions',
                                    'date_joined',
                                    'last_login',
                                    ]
            if not obj.is_verify_email:
                self.readonly_fields.append('is_active')
                tuple(self.readonly_fields)
        return super().get_readonly_fields(request, obj)

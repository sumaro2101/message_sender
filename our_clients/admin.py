from typing import Any
from django.contrib import admin

from mail_center.cache import get_or_set_cache
from .models import ClientServise


@admin.register(ClientServise)
class ClientServiseAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'employee',
                    'client_mail',
                    'client_first_name',
                    'client_last_name',
                    'client_middle_name',
                    'client_info',
                    'time_create',
                    'time_edit',
                    'actual',
                    ]
    list_filter = ('actual',)
    search_fields = ('employee',
                     'time_create',
                     'time_edit',
                     'client_mail',
                     'client_first_name',
                     'client_last_name',
                     'client_middle_name',
                     )

    def get_form(self,
                 request: Any,
                 obj: Any | None = ...,
                 change: bool = ...,
                 **kwargs: Any,
                 ) -> Any:
        form = super().get_form(request, obj, change, **kwargs)
        if get_or_set_cache(request.user.groups,
                            slug='moderator',
                            type_field='name',
                            ):
            form.base_fields['employee'].disabled = True
            form.base_fields['client_mail'].disabled = True
            form.base_fields['client_first_name'].disabled = True
            form.base_fields['client_last_name'].disabled = True
            form.base_fields['client_middle_name'].disabled = True
            form.base_fields['client_info'].disabled = True
        return form

from typing import Any
from django.contrib import admin

from mail_center.cache import get_or_set_cache
from .models import MessageInfo


@admin.register(MessageInfo)
class MessageInfoAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'employee',
                    'title_message',
                    'text_message',
                    'slug',
                    'time_create',
                    'time_edit',
                    'actual',
                    ]
    list_filter = ('actual',)
    search_fields = ('time_create', 'time_edit', 'title_message')

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
            form.base_fields['title_message'].disabled = True
            form.base_fields['text_message'].disabled = True
            form.base_fields['slug'].disabled = True
        return form

    prepopulated_fields = {'slug': ('employee', 'title_message')}

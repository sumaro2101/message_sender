from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Posts, PostComment
from mail_center.cache import get_or_set_cache


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'title',
                    'name_user',
                    'image',
                    'description',
                    'slug',
                    'views',
                    'likes',
                    'time_published',
                    'is_published',
                    'time_edit',
                    'is_edit',
                    'text_to_edit',
                    'comment_count',
                    )
    search_fields = ('pk',
                     'title',
                     'name_user',
                     'time_published',
                     )
    list_filter = 'is_edit',
    prepopulated_fields = {'slug': ('name_user', 'title')}

    def get_form(self,
                 request: Any,
                 obj: Any | None = ...,
                 change: bool = ...,
                 **kwargs: Any,
                 ) -> Any:
        form = super().get_form(request, obj, change, **kwargs)
        if get_or_set_cache(request.user.groups,
                            slug='content-manager',
                            type_field='name',
                            ):
            form.base_fields['title'].disabled = True
            form.base_fields['name_user'].disabled = True
            form.base_fields['image'].disabled = True
            form.base_fields['description'].disabled = True
            form.base_fields['slug'].disabled = True
            form.base_fields['likes'].disabled = True
            form.base_fields['time_edit'].disabled = True
            form.base_fields['is_edit'].disabled = True
            form.base_fields['text_to_edit'].disabled = True
            form.base_fields['comment_count'].disabled = True

        return form

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.select_related('name_user',)


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'parent',
                    'post',
                    'user_name',
                    'image',
                    'text',
                    'time_published',
                    'is_published',
                    'text_to_edit',
                    'time_edit',
                    'is_edit',
                    'likes',
                    )
    search_fields = ('post', 'user_name', 'time_published')
    list_filter = 'is_edit',

    def get_readonly_fields(self,
                            request: HttpRequest,
                            obj: Any | None = ...,
                            ) -> list[str] | tuple[Any, ...]:
        content_manager = get_or_set_cache(
            request.user.groups,
            slug='content-manager',
            type_field='name',
            )
        if content_manager:
            self.readonly_fields = ('post',
                                    'parent',
                                    'user_name',
                                    'image',
                                    'time_published',
                                    'time_edit',
                                    'is_edit',
                                    'likes',
                                    'text_to_edit',
                                    'text',
                                    )
        else:
            self.readonly_fields = ()
        return self.readonly_fields

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.select_related('post', 'parent', 'user_name')

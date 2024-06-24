from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Posts, PostComment
from mail_center.cache import get_or_set_cache
# Register your models here.

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
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        content_manager = get_or_set_cache(request.user.groups, slug='content-manager', type_field='name')
        if content_manager:
            self.readonly_fields = (
                                    'image',
                                    'views',
                                    'description',
                                    'likes',
                                    'time_published',
                                    'time_edit',
                                    'is_edit',
                                    'text_to_edit',
                                    'comment_count',
                                    )
        else:
            self.readonly_fields = ()
        return self.readonly_fields
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]: 
        queryset = super().get_queryset(request)
        return queryset.select_related('name_user',)

    list_filter = 'is_edit',
    
    prepopulated_fields = {'slug': ('name_user', 'title')}
    
    
    
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
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        content_manager = get_or_set_cache(request.user.groups, slug='content-manager', type_field='name')
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
    
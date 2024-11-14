from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  )
from django.views.generic.edit import ModelFormMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin,
                                        )

from blog.models import Posts, PostComment
from .forms import AddPostForm, AddCommentForm
from mail_center.cache import get_or_set_cache

from pytils.translit import slugify


class PostsListView(ListView):
    model = Posts
    context_object_name = 'posts'

    paginate_by = 3
    extra_context = {'title': 'Electronic Shop', 'catg_selected': 7}

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = (queryset
                    .filter(Q(is_published=True))
                    .select_related('name_user'))
        return queryset


class PostDetailView(ModelFormMixin, DetailView):
    model = Posts
    form_class = AddCommentForm
    context_object_name = 'post'
    slug_url_kwarg = 'slug_id'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        return queryset.select_related('name_user')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return self.object

    def get_context_data(self,
                         *,
                         object_list=None,
                         **kwargs,
                         ):
        content_manager = get_or_set_cache(
            self.request.user.groups,
            slug='content-manager',
            type_field='name',
            )
        moderator = get_or_set_cache(
            self.request.user.groups,
            slug='moderator',
            type_field='name',
            )
        context = super().get_context_data(**kwargs)
        context['title'] = 'Electronic Shop'
        context['catg_selected'] = 7
        context['comments'] = (PostComment.objects
                               .filter(Q(post=kwargs['object']))
                               .select_related('parent',
                                               'user_name',
                                               'post',
                                               ))
        context['content_manager'] = content_manager
        context['moderator'] = moderator

        return context

    def post(self, request, *args, **kwargs):
        check_values = request.POST
        post = self.get_object()
        if check_values.get('text'):
            comment_to_post = AddCommentForm(data=request.POST)
            if comment_to_post.is_valid():
                comment = comment_to_post.save(commit=False)
                comment.post = post
                comment.user_name = self.request.user
                comment.save()
                post.comment_count += 1
                post.save(update_fields=['comment_count'])
            else:
                pass
        elif check_values.get('publish'):
            if post.is_published:
                post.is_published = False
                post.save(update_fields=['is_published'])
            else:
                post.is_published = True
                post.save(update_fields=['is_published'])
        elif check_values.get('get_block_comment'):
            comment = (PostComment.objects.
                       filter(pk=check_values.get('get_block_comment'))
                       .first())
            if not comment:
                return redirect('blog:post', post.slug)
            else:
                comment.is_published = False
                comment.save(update_fields=['is_published'])
        return redirect('blog:post', post.slug)


class AddPostCreateView(LoginRequiredMixin,
                        UserPassesTestMixin,
                        CreateView):
    model = Posts
    form_class = AddPostForm
    template_name = 'blog/posts_form.html'
    extra_context = {'title': 'Electronic Shop', 'catg_selected': 7}

    def form_valid(self, form):
        form.instance.name_user = self.request.user
        slug_name = slugify(form.instance.name_user)
        slug_title = slugify(form.instance.title)
        form.instance.slug = f'{slug_name}-{slug_title}'
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        return (not self.request.user.is_staff or
                self.request.user.is_superuser)


class UpdatePostView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     UpdateView):
    model = Posts
    context_object_name = 'post'
    form_class = AddPostForm
    slug_url_kwarg = 'slug_id'
    template_name = 'blog/posts_form.html'
    extra_context = {'title': 'UpdatePost', 'catg_selected': 7}

    def form_valid(self, form):
        form.instance.is_edit = True
        form.instance.time_edit = timezone.now()
        slug_name = slugify(form.instance.name_user)
        slug_title = slugify(form.instance.title)
        form.instance.slug = f'{slug_name}-{slug_title}'
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return (self.request.user == obj.name_user or
                self.request.user.is_superuser)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Posts
    context_object_name = 'post'
    slug_url_kwarg = 'slug_id'
    success_url = reverse_lazy('blog:posts')

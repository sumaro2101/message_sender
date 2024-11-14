from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator, decorator_from_middleware
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_bytes
from django.middleware.csrf import CsrfViewMiddleware
from django.views.generic import (TemplateView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  ListView
                                  )
from django.contrib.auth import get_user_model, mixins
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (LoginView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView,
                                       PasswordContextMixin
                                       )

from typing import Any

from users.mixins import RequiredNotAuthenticatedMixin
from .forms import (UserChangePasswordForm,
                    UserLoginForm,
                    RegisterUserForm,
                    UserUpdateForm)
from users.tasks import send_verify_email
from mail_center.cache import get_or_set_cache

import random


csrf_protect = decorator_from_middleware(CsrfViewMiddleware)

VERIFY_EMAIL_SESSION_TOKEN = '_verify_session_token'


class UserDetailView(DetailView):
    model = get_user_model()
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'current_user'

    def post(self, request: HttpRequest, *args: str, **kwargs):
        obj = self.get_object()

        if not obj.is_verify_email:
            return redirect('users:user', **{
                'username': self.kwargs['username'],
                })

        if obj.is_active:
            obj.is_active = False
        else:
            obj.is_active = True

        obj.save(update_fields=['is_active'])

        return redirect('users:user', **{
            'username': self.kwargs['username']},
                        )

    def get_context_data(self, **kwargs):
        content_manager = get_or_set_cache(
            self.request.user.groups,
            slug='content-manager',
            type_field='name',
            )
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        context['content_manager'] = content_manager
        return context


class UserListView(mixins.LoginRequiredMixin,
                   mixins.UserPassesTestMixin,
                   ListView):
    model = get_user_model()
    context_object_name = 'users'
    paginate_by = 30

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(is_superuser=False) &
                                   Q(is_staff=False)).order_by('-is_active')
        return queryset

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser or self.request.user.is_staff


class AuthView(RequiredNotAuthenticatedMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    extra_context = {'title': 'Authentication'}

    def get_success_url(self) -> str:
        return reverse_lazy('mail_center:mails')


class RegisterUser(mixins.UserPassesTestMixin,
                   PasswordContextMixin,
                   CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register_user.html'
    email_template_name = "check_mail/register_check_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy('users:done')
    title = ('Завершение регистрации')
    token_generator = default_token_generator
    extra_context = {'title': 'Registration'}

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        form.instance.is_active = False
        form.save()

        user = get_user_model()._default_manager.get(email=email)
        username = user.username
        current_site = 'localhost'
        site_name = 'Messender'
        update_session_auth_hash(self.request, user)

        context = {
                "email": email,
                "domain": current_site,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": username,
                "token": self.token_generator.make_token(user),
                "protocol": "https" if self.request.is_secure() else "http",
            }

        send_verify_email.apply_async(
            kwargs={'email': email,
                    'context': context,
                    'email_template_name': 'check_mail/register_check_email.html',
                    })

        self.object = form
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self) -> bool | None:
        return (not self.request.user.is_authenticated or
                self.request.user.is_superuser or
                self.request.user.is_staff)


class UserConfirmEmailView(RequiredNotAuthenticatedMixin, TemplateView):
    template_name = 'check_mail/verify_done.html'
    reset_url_token = "verify_email"
    token_generator = default_token_generator
    extra_context = {'title': 'ConfirmEmail'}

    def dispatch(self, *args, **kwargs):
        self.valid = False
        self.user = self.get_user(kwargs['uidb64'])
        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(
                    VERIFY_EMAIL_SESSION_TOKEN,
                    )
                if self.token_generator.check_token(
                   self.user, session_token,
                   ):
                    self.valid = True
                    self.user.is_active = True
                    self.user.is_verify_email = True
                    self.user.save(update_fields=(
                        'is_active',
                        'is_verify_email',
                        ))
                    del self.request.session[VERIFY_EMAIL_SESSION_TOKEN]
            else:
                if self.token_generator.check_token(self.user, token):
                    self.request.session[VERIFY_EMAIL_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        uid = urlsafe_base64_decode(uidb64).decode()
        try:
            user = get_user_model()._default_manager.get(pk=uid)
        except:
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_valid'] = self.valid
        if self.valid:
            context['message'] = 'Регистрация завершена!'
        else:
            context['message'] = 'Регистрация не может быть завершена'
        return context


class UserRegistrationDode(RequiredNotAuthenticatedMixin, TemplateView):
    template_name = 'check_mail/register_done.html'


class UpdateProfileUser(mixins.LoginRequiredMixin,
                        mixins.UserPassesTestMixin,
                        UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    context_object_name = 'user_edit'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/change_profile.html'
    extra_context = {'title': 'UpdateProfile'}

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return self.request.user == obj or self.request.user.is_superuser

    def get_success_url(self) -> str:
        return reverse_lazy('users:user',
                            kwargs={
                                'username': self.kwargs.get('username'),
                                },
                            )


class UserChoiceWayView(TemplateView):
    template_name = 'passwords/password_choice_way.html'


class UserChangePassword(PasswordChangeView):
    form_class = UserChangePasswordForm
    template_name = 'passwords/password_change_form.html'
    success_url = reverse_lazy("users:password_change_done")
    extra_context = {'title': 'ChangePassword'}


class UserChangePasswordDone(PasswordChangeDoneView):
    template_name = 'passwords/password_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_session_auth_hash(self.request, self.request.user)
        context["title"] = 'Done'
        return context


class UserResetPassword(PasswordResetView):
    template_name = 'passwords/password_reset_form.html'
    email_template_name = 'passwords/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserResetPasswordDone(PasswordResetDoneView):
    template_name = 'passwords/password_reset_done.html'


class UserResetPasswordConfirm(PasswordResetConfirmView):
    template_name = 'passwords/password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")


class UserResetPasswordComplete(PasswordResetCompleteView):
    template_name = 'passwords/password_reset_complete.html'


class UserPasswordTemporary(PasswordResetView):
    template_name = 'passwords/password_reset_form.html'
    email_template_name = 'passwords/password_temporary_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    extra_context = {'title': 'Reset', 'is_temporary': True}


class UserPasswordTemporaryDone(PasswordResetConfirmView):
    template_name = 'passwords/password_temporary_done.html'
    password_value = int_to_base36(random.getrandbits(41))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user(self.kwargs["uidb64"])
        user.set_password(self.password_value)
        user.save(update_fields=('password',))

        context['title'] = 'Done'
        context['temporary_password'] = self.password_value
        return context

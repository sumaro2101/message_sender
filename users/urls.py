from django.urls import path

from users.apps import UsersConfig
from . import views
from django.contrib.auth.views import LogoutView


app_name = UsersConfig.name


urlpatterns = [
    # login - logout
    path('login/',
         views.AuthView.as_view(),
         name='login'),
    path('logout/',
         LogoutView.as_view(),
         name='logout',
         ),
    # registration
    path('regisration/',
         views.RegisterUser.as_view(),
         name='reg',
         ),
    path('regisration/done/',
         views.UserRegistrationDode.as_view(),
         name='done',
         ),
    path('regisration/verify/<uidb64>/<token>/',
         views.UserConfirmEmailView.as_view(),
         name='verify_email',
         ),
    # user
    path('users/',
         views.UserListView.as_view(),
         name='users_list',
         ),
    path('user/<str:username>/',
         views.UserDetailView.as_view(),
         name='user',
         ),
    path('user/<str:username>/update/',
         views.UpdateProfileUser.as_view(),
         name='update',
         ),
    # password_gate
    path('password_way/',
         views.UserChoiceWayView.as_view(),
         name='password_way',
         ),
    # password_change
    path('password_change/',
         views.UserChangePassword.as_view(),
         name='password_change',
         ),
    path('password_change/done/',
         views.UserChangePasswordDone.as_view(),
         name='password_change_done',
         ),
    # password_reset
    path('password_reset/',
         views.UserResetPassword.as_view(),
         name='password_reset',
         ),
    path('password_reset/done/',
         views.UserResetPasswordDone.as_view(),
         name='password_reset_done',
         ),
    path('password_reset/complete/',
         views.UserResetPasswordComplete.as_view(),
         name='password_reset_complete',
         ),
    path('password_reset/<uidb64>/<token>/',
         views.UserResetPasswordConfirm.as_view(),
         name='password_reset_confirm',
         ),
    path('password_temporary/',
         views.UserPasswordTemporary.as_view(),
         name='verify_temporary',
         ),
    path('password_temporary_done/<uidb64>/<token>/',
         views.UserPasswordTemporaryDone.as_view(),
         name='verify_temporary_done',
         ),
]

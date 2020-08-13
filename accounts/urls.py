from django.urls import path
from . import views
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
                                       )


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('reset/', PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/confirm', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
    path('settings/password/', PasswordChangeView.as_view(
        template_name='registration/password_change.html'),
        name='password_change'),
    path('settings/password/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'),
        name='password_change_done'),
]
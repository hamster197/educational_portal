from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include, reverse_lazy

from core.views import LoginPage, StudentRegisterPage

app_name = 'core_urls'

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(), name='logout_url'),

    path('password_reset_start/', PasswordResetView.as_view(template_name='core/account/password_reset_form.html',
                                                            email_template_name='core/account/password_reset_email.html',
                                                            success_url=reverse_lazy(
                                                                'core_urls:reset_password_done')),
         name='reset_password_url'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='core/account/password_reset_done_form.html'),
         name='reset_password_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='core/account/password_reset_confim_form.html', success_url=reverse_lazy(
        'core_urls:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='core/account/password_reset_complete.html'),
         name='password_reset_complete'),

    path('register/', StudentRegisterPage.as_view(), name='registration_student_url'),

    path('api/v1/', include('core.api.urls'),)
]

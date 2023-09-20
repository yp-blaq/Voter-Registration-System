from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
path('', views.register_request, name = 'register'),
path('login', views.login_request, name='login'),
path('logout', views.logout_request, name='logout'),
path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
# Forget Password
path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             #subject_template_name='password-reset_form.html/password_reset_subject.txt',
             #email_template_name='password-reset_form.html/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
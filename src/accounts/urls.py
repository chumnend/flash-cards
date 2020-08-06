from django.contrib.auth import views as auth_views
from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path(
        'login/', 
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ), 
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html', 
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'
        ), 
        name='password_reset'
    ),
    path(
        'reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ), 
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ), 
        name='password_reset_confirm'
    ),
    path(
        'reset/complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ), 
        name='password_reset_complete'
    ),
    path(
        'change/', 
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change.html'
        ), 
        name='password_change',
    ),
    path(
        'change/done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ), 
        name='password_change_done',
    ),
    path('user/<int:pk>/', views.profile, name="profile"),
    path('user/<int:pk>/follow', views.follow, name="follow"),
    path('user/<int:pk>/unfollow', views.unfollow, name="unfollow"),
]

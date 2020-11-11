from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('signup/done', views.SignupDone.as_view(), name='signup-done'),
    path('signup/complete/<token>/', views.SignupComplete.as_view(), name='signup-complete'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('setting/', views.Setting.as_view(), name='setting'),
    path('email/change/', views.EmailChange.as_view(), name='email-change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email-change-done'),
    path('email/change/complete/<token>/', views.EmailChangeComplete.as_view(), name='email-change-complete'),
    path('password_change/', views.PasswordChange.as_view(), name='password-change'),
    path('password_reset/', views.PasswordReset.as_view(), name='password-reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password-reset-done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password-reset-complete'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user-update'),
    path('user_detail/<int:pk>/comment', views.UserDetailComment.as_view(), name='user-comment'),
]


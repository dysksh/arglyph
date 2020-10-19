from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('signup/done', views.SignupDone.as_view(), name='signup-done'),
    path('signup/complete/<token>/', views.SignupComplete.as_view(), name='signup-complete'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name="logout"),
]


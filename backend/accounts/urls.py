# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('verify-token/', views.VerifyTokenView.as_view(), name='verify_token'),
]

from django.urls import path
from .views import RegisterView, LoginView, JWTVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('jwt-verify/', JWTVerifyView.as_view(), name='jwt-verify'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notebooks', views.NotebookViewSet, basename='notebook')

urlpatterns = [
    path('', include(router.urls)),
]
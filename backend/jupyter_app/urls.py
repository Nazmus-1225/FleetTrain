from django.urls import path, include
from rest import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notebook', views.NotebookViewSet, basename='notebook')

urlpatterns = [
    path('', include(router.urls)),
]
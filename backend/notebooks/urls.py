from django.urls import path
from . import views

urlpatterns = [
    path('api/notebooks/create', views.create_notebook, name='create_notebook'),
    path('api/notebooks/<str:notebook_id>/execute', views.execute_code, name='execute_code'),
    path('api/notebooks/<str:notebook_id>/save', views.save_notebook, name='save_notebook'),
]

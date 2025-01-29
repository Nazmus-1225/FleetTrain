from django.urls import path
from . import views
from .views import NotebookListView, NotebookDeleteView, NotebookCreateView, NotebookOpenView

urlpatterns = [
    path('create/', NotebookCreateView.as_view(), name='create_notebook'),
    path('all/',NotebookListView.as_view(),name='notebook_list'),
    path('delete/<int:pk>/', NotebookDeleteView.as_view(), name='notebook-delete'),
    path('open/<int:pk>/', NotebookOpenView.as_view(), name='notebook-open')
]

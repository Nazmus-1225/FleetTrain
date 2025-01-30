from django.urls import path
from . import views
from .views import NotebookListView, ExecuteCodeView,NotebookDeleteView, NotebookCreateView, NotebookOpenView, NotebookCloseView, DownloadFilesView,DatasetUploadView, DownloadNotebooksView, FetchFilesView

urlpatterns = [
    path('create/', NotebookCreateView.as_view(), name='create_notebook'),
    path('all/',NotebookListView.as_view(),name='notebook_list'),
    path('delete/<int:pk>/', NotebookDeleteView.as_view(), name='notebook-delete'),
    path('open/<int:pk>/', NotebookOpenView.as_view(), name='notebook-open'),
    path('close/<int:pk>/', NotebookCloseView.as_view(), name='notebook-close'),
    path('upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('getFiles/<int:pk>/',FetchFilesView.as_view(), name='fetch-files'),
    path('download/<int:pk>/',DownloadNotebooksView.as_view(), name='download-notebook'),
    path('download/<int:pk>/<str:filename>/',DownloadFilesView.as_view(), name='download-file'),
    path('execute/',ExecuteCodeView.as_view(), name='execute-code')
]

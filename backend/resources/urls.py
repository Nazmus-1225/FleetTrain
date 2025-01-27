from django.urls import path
from .views import ResourceCreateView, ResourceDeleteView, ResourceListView, KernelListView
urlpatterns = [
    path('all/', ResourceListView.as_view(), name='resource-list'),
    path('create/', ResourceCreateView.as_view(), name='resource-create'),
    path('delete/<int:pk>/', ResourceDeleteView.as_view(), name='resource-delete'),
    path('kernels/', KernelListView.as_view(), name='kernel-list'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.collection_list, name='collection_list'),
    path('create/', views.collection_create, name='collection_create'),
    path('<int:pk>/', views.collection_detail, name='collection_detail'),
    path('<int:pk>/edit/', views.collection_edit, name='collection_edit'),
    path('<int:pk>/delete/', views.collection_delete, name='collection_delete'),
    path('<int:pk>/history/', views.collection_history, name='collection_history'),
    path('<int:pk>/pdf/', views.collection_pdf, name='collection_pdf'),
]
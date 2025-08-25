from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router= DefaultRouter()

urlpatterns = [
    path('system-info/', views.system_info_upsert, name='system-info-upsert'),
    path('system-info/<str:hostname>/', views.system_info_get, name='system-info-get'),
    path('system-info-list/', views.system_info_list, name='system-info-list'),
    path('processes/bulk/', views.processes_bulk, name='processes-bulk'),
    path('processes/', views.processes_query, name='processes-query'),
   
]
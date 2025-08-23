from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router= DefaultRouter()
urlpatterns = [
    path('system-info/', views.system_info_upsert, name='system-info-upsert'), #to post system info
    path('system-info/<str:hostname>/', views.system_info_get, name='system-info-get'), # to get system info by hostname
    path('system-info-list/', views.system_info_list, name='system-info-list'), # to get system info list
    path('processes/bulk/', views.processes_bulk, name='processes-bulk'),  # to post process
    path('processes/', views.processes_query, name='processes-query'), #to get process info
    path('', views.index_view, name='index'),# frontend
]
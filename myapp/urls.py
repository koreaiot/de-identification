from django.urls import path

from . import views

urlpatterns = [
    path('excel', views.download_excel, name='download_excel'),
    path('zip_json_excel', views.zip_json_excel, name='zip_json_excel'),
    path('zip_json_upload', views.zip_json_upload, name='zip_json_upload'),
    path('progress', views.progress, name='progress'),
]


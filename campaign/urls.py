from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<slug:pk>/', views.UpdateFile.as_view(), name='edit'),
    path('delete/post/<slug:pk>/', views.DeleteFile.as_view(), name='delete'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('pdf/<int:blog_id>/', views.generate_pdf, name='pdf'),
    path('pdf/', views.generate_all_pdf, name='all_pdf'),
    re_path('^csv-uploader/$', views.CsvUploader.as_view(), name='csv_uploader'),
    #path('table/', views.table__, name='table'),
]

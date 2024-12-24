# file_upload/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Định nghĩa URL cho trang upload_file
    path('', views.upload_file_ocr, name='ocr_data'),
    path('register/', views.register, name='register'),
    path('annotate/', views.upload_and_annotate, name='annotate'),
    path('get_images/', views.get_images, name='get_images'),
    path('delete_images/', views.delete_images, name='delete_images'),
]

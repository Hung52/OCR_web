# file_upload/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Định nghĩa URL cho trang upload_file
    path('', views.upload_file_ocr, name='ocr_data'),
    path('register/', views.register, name='register'),
    path('annotate/', views.upload_and_annotate, name='annotate'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
]
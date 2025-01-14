"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, include
from ocr_data import views

urlpatterns = [
    # Trang chủ (home)
    path('', views.home, name='home'),
    
    # Đăng nhập/đăng xuất
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login?logged_out=true'), name='logout'),

    path('upload_file_ocr/', views.upload_file_ocr, name='upload_file_ocr'),

    # Bao gồm các URL từ file_upload
    path('upload/', include('ocr_data.urls')),

    path('delete_images/', views.delete_images, name='delete_images'),
    path('get_images/', views.get_images, name='get_images'),

    # Đăng ký các URL liên quan đến tài khoản người dùng Django
    path('accounts/', include('django.contrib.auth.urls')),
]

# Cung cấp URL tĩnh (static) trong môi trường phát triển (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
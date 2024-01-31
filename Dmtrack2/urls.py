"""Dmtrack2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from django.views.generic.base import TemplateView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenVerifyView)
from userapp.views import MyTokenObtainPairView
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('user/', include('userapp.urls')),#demo add,
    path('dmtrack/', include('backend.urls')),#demo add,
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # rest_framework_simplejwt自带的得到token
    # 登录获取刷新token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #path("docs/", include_docs_urls(title="DRF API文档", description="Django REST framework")),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

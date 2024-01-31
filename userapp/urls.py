from django.urls import path,include
from rest_framework.routers import DefaultRouter
from userapp import views
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),# DRF的api

]


from django.urls import path,include

from rest_framework.routers import DefaultRouter

from backend import views
router = DefaultRouter()
##router.register(prefix="viewsets", viewset=views.HomeDataViewsets)##viewsets 路由

urlpatterns = [
    # Function Based View
    #path("home/", views.HomeData2.as_view(), name="home_data"),
    path("SamplingData/", views.SamplingGeneric.as_view(), name="SamplingGeneric"),
    path("SamplingData/<int:pk>/", views.SamplingGeneric.as_view(), name="SamplingGet"),
    path("StrainInfoData/", views.StrainInfoGeneric.as_view(), name="StrainInfoGeneric"),
    path("StrainInfoData/<int:pk>/", views.StrainInfoGeneric.as_view(), name="StrainInfoGet"),
    path("SequencingData/", views.SequencingGeneric.as_view(), name="SequencingGeneric"),
    path("SequencingData/<int:pk>/", views.SequencingGeneric.as_view(), name="SequencingGet"),
    path("tools_sp/", views.Tools_SP.as_view(), name="tools_sp"),
    path("tools_ep/", views.Tools_GENE.as_view(), name="tools_ep"),
    path('', include(router.urls)),# DRF的api
]

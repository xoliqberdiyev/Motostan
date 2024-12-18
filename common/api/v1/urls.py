from django.urls import path, include

from common.api.v1 import views

urlpatterns = [
    path('about-us/', views.AboutUsApiView.as_view(), name='about-us'),
    path('advertisement/', views.AdvertisementApiView.as_view(), name='advertisement-list'),
    path('banner/', views.BannerApiView.as_view(), name='banner-list'),
]
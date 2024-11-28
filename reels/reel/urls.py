from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download/', views.download_reel, name='download_reel'),
    path('api/download/', views.download_reel, name='download_reel_api'),
]

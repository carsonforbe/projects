from django.urls import path
from . import views

urlpatterns = [
    path('', views.bus_schedule, name='bus_schedule'),  # This is the URL for the bus schedule page
]

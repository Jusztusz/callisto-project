from django.urls import path 
from . import views

urlpatterns = [
    path("", views.network, name="network")
]
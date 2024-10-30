from django.urls import path
from . import views

urlpatterns = [
    path('', views.alert, name='alert'),  # A gyökér URL a hardware nézethez
]
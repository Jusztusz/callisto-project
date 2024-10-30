from django.urls import path
from . import views

urlpatterns = [
    path('', views.hardware, name='hardware'),  # A gyökér URL a hardware nézethez
    path('get_new_data/', views.get_new_data, name='get_new_data'),  # Az új nézet
]
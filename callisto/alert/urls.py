from django.urls import path
from . import views

urlpatterns = [
    path('', views.alert, name='alert'),
    path('delete_alert/<int:alert_id>/', views.delete_alert, name='delete_alert'),
    path('get_telegram_credentials/', views.get_telegram_credentials, name='get_telegram_credentials'),
    path('delete_credential/<str:chat_id>/', views.delete_credential, name='delete_credential'),
]
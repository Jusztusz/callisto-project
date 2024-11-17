from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.control_panel, name='control_panel'),
    path('toggle-cm-agent/', views.toggle_cm_agent, name='toggle_cm_agent'),
    path('toggle-alert-agent/', views.toggle_alert_agent, name='toggle_alert_agent'),
]
from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/hardware/', consumer.CPUConsumer.as_asgi()),
]
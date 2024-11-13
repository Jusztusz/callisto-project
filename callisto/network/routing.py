from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/network/', consumer.networkConsumer.as_asgi()),
]
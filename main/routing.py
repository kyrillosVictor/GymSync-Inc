from django.urls import path

from consumers import NotificationConsumer

#from channels.routing import route

ws_patterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi())
]
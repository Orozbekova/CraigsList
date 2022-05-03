from django.template.defaulttags import url

from . import consumers
from django.urls import path

websocket_urlpatterns = [
    # path('ws/index/', consumers.SyncView.as_asgi())
    url(r'^ws/index', consumers.SyncView.as_asgi())
]

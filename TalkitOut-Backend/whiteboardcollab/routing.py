from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/whiteboardcollab/(?P<room_name>\w+)/$",
        consumers.whiteboardcollabConsumer.as_asgi(),
    ),
]

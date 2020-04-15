#awais code commented by ahmed as it condlicts my web sockets 

# from channels.routing import ProtocolTypeRouter, URLRouter
# import OSINT_System_Core.routing

# application = ProtocolTypeRouter({
#     'http': URLRouter(OSINT_System_Core.routing.urlpatterns),
# })

##########################################

#ahmed code 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from .consumers import ChartConsumers,HashtagConsumers
websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', ChartConsumers),
      re_path(r'ws/chat/$', ChartConsumers),
      re_path(r'ws/dashboard_hastags_worldwide/$', HashtagConsumers),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

#ahmed code end
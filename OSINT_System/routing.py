from channels.routing import ProtocolTypeRouter, URLRouter
import OSINT_System_Core.routing

application = ProtocolTypeRouter({
    'http': URLRouter(OSINT_System_Core.routing.urlpatterns),
})
"""
from channels.routing import route
from chat import consumer

channel_routing = [
    route("websocket.connect", consumers.ws_connect ),
    route("websocket.receive", consumers.ws_receive),
    route("websocket.disconnect", consumers.ws_disconnect),
]
"""
from channels import route
from post.consumers import connect_blog, disconnect_blog, save_post


# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. WebSocket messages of all
# types have a 'path' attribute, so we're using that to route the socket.
# While this is under stream/ compared to the HTML page, we could have it on the
# same URL if we wanted; Daphne separates by protocol as it negotiates with a browser.
channel_routing = [
    # Called when incoming WebSockets connect  [^/]+
    route("websocket.connect", connect_blog, path=r'^/curso.com/(?P<id_video>[0-9]+)/(?P<slug>[^/]+)/stream/$'),

    # Called when the client closes the socket
    route("websocket.disconnect", disconnect_blog, path=r'^/curso.com/(?P<id_video>[0-9]+)/(?P<slug>[^/]+)/stream/$'),

    # Called when the client sends message on the WebSocket
    route("websocket.receive", save_post, path=r'^/curso.com/(?P<id_video>[0-9]+)/(?P<slug>[^/]+)/stream/$'),
	
    # A default "http.request" route is always inserted by Django at the end of the routing list
    # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
    # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
    # fall through to normal views.
]


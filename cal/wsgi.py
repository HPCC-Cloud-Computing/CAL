from wsgiref import simple_server

import falcon
from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import netutils
import six
import socket

from cal import base
from cal.v1 import compute
from cal.v1 import network
from cal.v1 import storage

CONF = cfg.CONF

_WSGI_OPTIONS = (
    cfg.IPOpt('host', default='127.0.0.1',
              help='Address on which the self-hosting server will listen.'),

    cfg.PortOpt('port', default=8888,
                help='Port on which the self-hosting server will listen.'),
)

CONF.register_opts(_WSGI_OPTIONS)

LOG = logging.getLogger(__name__)


class FuncMiddleware(base.BaseMiddleware):

    def __init__(self, func):
        super(FuncMiddleware, self).__init__()
        self.func = func

    def process_resource(self, req, resp, resource, params):
        return self.func(req, resp, params)


class WSGIDriver(object):

    def __init__(self):
        self.app = None
        self._init_routes_and_middlewares()

    def before_hooks(self):
        """Exposed to facilitate unit testing."""
        return [
            # Some hook methods
        ]

    def _init_routes_and_middlewares(self):
        """Initialize hooks and URI routes to resources."""
        middleware = [FuncMiddleware(hook) for hook in self.before_hooks()]
        # If you have another Middleware, like BrokeMiddleware for e.x
        # You can append this to middleware:
        # middleware.append(BrokeMiddleware)
        self.app = falcon.API(middleware=middleware)

        endpoints = network.public_endpoint(self, CONF)
        endpoints += compute.public_endpoint(self, CONF)
        endpoints += storage.public_endpoint(self, CONF)

        for route, resource in endpoints:
            self.app.add_route(route, resource)

    def _error_handler(self, exc, request, response, params):
        if isinstance(exc, falcon.HTTPError):
            raise exc
        LOG.exception(exc)
        raise falcon.HTTPInternalServerError('Internal server error',
                                             six.text_type(exc))

    def _get_server_cls(self, host):
        """Return an appropriate WSGI server class base on provided host
        :param host: The listen host for the zaqar API server.
        """
        server_cls = simple_server.WSGIServer
        if netutils.is_valid_ipv6(host):
            if getattr(server_cls, 'address_family') == socket.AF_INET:
                class server_cls(server_cls):
                    address_family = socket.AF_INET6
        return server_cls

    def listen(self):
        """Self-host using 'bind' and 'port' from the WSGI config group."""

        msgtmpl = (u'Serving on host %(host)s:%(port)s')
        host = getattr(CONF, 'host', '127.0.0.1')
        port = getattr(CONF, 'port', 8888)
        LOG.info(msgtmpl,
                 {'host': host, 'port': port})
        server_cls = self._get_server_cls(host)
        httpd = simple_server.make_server(host,
                                          port,
                                          self.app,
                                          server_cls)
        httpd.handle_request()

from wsgiref import simple_server

import falcon
from oslo_log import log as logging
from oslo_utils import netutils
import six
import socket

import cal.conf
from cal import base
from cal import utils
from cal.v1 import compute
from cal.v1 import network
from cal.v1 import storage

CONF = cal.conf.CONF

LOG = logging.getLogger(__name__)


class FuncMiddleware(base.BaseMiddleware):

    def __init__(self, func):
        super(FuncMiddleware, self).__init__()
        self.func = func

    def process_request(self, req, resp):
        deserializer = utils.JSONRequestDeserializer()
        if deserializer.has_body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON doc is required')

        body = deserializer.default(req)
        cloud = body.get('cloud')
        req.environ['cal.cloud'] = cloud

    def process_resource(self, req, resp, resource, params):
        return self.func(req, resp, params)


class WSGIDriver(object):

    def __init__(self):
        self.app = None
        self.endpoints = None
        self.middleware = None
        self._init_routes_and_middlewares()

    def before_hooks(self):
        """Exposed to facilitate unit testing."""
        return [
            # Some hook methods
        ]

    def _init_endpoints(self):
        """Initialize URI routes to resources"""
        self.endpoints = network.public_endpoint(self, CONF)
        self.endpoints += compute.public_endpoint(self, CONF)
        self.endpoints += storage.public_endpoint(self, CONF)

    def _init_middlewares(self):
        """Initialize hooks and middlewares
        If you have another Middleware, like BrokeMiddleware for e.x
        You can append this to middleware:
        self.middleware.append(BrokeMiddleware)
        """
        self.middleware = \
            [FuncMiddleware(hook) for hook in self.before_hooks()]

    def _init_routes_and_middlewares(self):
        """Initialize hooks and URI routes to resources."""
        self._init_middlewares()
        self._init_endpoints()

        self.app = falcon.API(middleware=self.middleware)

        for route, resource in self.endpoints:
            self.app.add_route(route, resource)

    def _error_handler(self, exc, request, response, params):
        """Handler error"""
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
        host = CONF.wsgi.wsgi_host
        port = CONF.wsgi.wsgi_port
        LOG.info(msgtmpl,
                 {'host': host, 'port': port})
        server_cls = self._get_server_cls(host)
        httpd = simple_server.make_server(host,
                                          port,
                                          self.app,
                                          server_cls)
        httpd.serve_forever()

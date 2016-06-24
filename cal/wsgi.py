# Define all abstract wsgi class
import routes
import webob.dec
import webob.exc
import routes.middleware
import six
import sys
import json
import datetime


class Request(webob.Request):
    """
    Techbk: Cover webob.Request class.
    """
    pass


class Router(object):
    """
    Techbk: Copy from nova.wsgi
    WSGI middleware that maps incoming requests to WSGI apps.
    """

    def __init__(self, mapper):
        """Create a router for the given routes.Mapper.

        Each route in `mapper` must specify a 'controller', which is a
        WSGI app to call.  You'll probably want to specify an 'action' as
        well and have your controller be an object that can route
        the request to the action-specific method.

        Examples:
          mapper = routes.Mapper()
          sc = ServerController()

          # Explicit mapping of one route to a controller+action
          mapper.connect(None, '/svrlist', controller=sc, action='list')

          # Actions are all implicitly defined
          mapper.resource('server', 'servers', controller=sc)

          # Pointing to an arbitrary WSGI app.  You can specify the
          # {path_info:.*} parameter so the target app can be handed just that
          # section of the URL.
          mapper.connect(None, '/v1.0/{path_info:.*}', controller=BlogApp())

        """
        self.map = mapper
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                          self.map)

    # Copy from Example
    # @classmethod
    # def factory(cls, global_conf, **local_conf):
    #     return cls(APIMapper())

    @webob.dec.wsgify(RequestClass=Request)  # nova.wsgi
    def __call__(self, req):
        """Route the incoming request to a controller based on self.map.

        If no match, return a 404.

        """
        return self._router

    @staticmethod
    @webob.dec.wsgify(RequestClass=Request)  # nova.wsgi
    def _dispatch(req):
        """Dispatch the request to the appropriate controller.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.

        """
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app





class Application(object):
    """
    Techbk: Copy from nova.api
    Base WSGI application wrapper. Subclasses need to implement __call__."""

    @classmethod
    def factory(cls, global_config, **local_config):
        """Used for paste app factories in paste.deploy config files.

        Any local configuration (that is, values under the [app:APPNAME]
        section of the paste config) will be passed into the `__init__` method
        as kwargs.

        A hypothetical configuration would look like:

            [app:wadl]
            latest_version = 1.3
            paste.app_factory = nova.api.fancy_api:Wadl.factory

        which would result in a call to the `Wadl` class as

            import nova.api.fancy_api
            fancy_api.Wadl(latest_version='1.3')

        You could of course re-implement the `factory` method in subclasses,
        but using the kwarg passing it shouldn't be necessary.

        """
        return cls(**local_config)

    def __call__(self, environ, start_response):
        r"""Subclasses will probably want to implement __call__ like this:

        @webob.dec.wsgify(RequestClass=Request)
        def __call__(self, req):
          # Any of the following objects work as responses:

          # Option 1: simple string
          res = 'message\n'

          # Option 2: a nicely formatted HTTP exception page
          res = exc.HTTPForbidden(explanation='Nice try')

          # Option 3: a webob Response object (in case you need to play with
          # headers, or you want to be treated like an iterable, or ...)
          res = Response()
          res.app_iter = open('somefile')

          # Option 4: any wsgi app to be run next
          res = self.application

          # Option 5: you can get a Response object for a wsgi app, too, to
          # play with headers etc
          res = req.get_response(self.application)

          # You can then just return your response...
          return res
          # ... or set req.response and return None.
          req.response = res

        See the end of http://pythonpaste.org/webob/modules/dec.html
        for more info.

        """
        # raise NotImplementedError(_('You must implement __call__'))
        raise NotImplementedError('You must implement __call__')


class Middleware(Application):
    """Base WSGI middleware.

    These classes require an application to be
    initialized that will be called next.  By default the middleware will
    simply call its wrapped app, or you can override __call__ to customize its
    behavior.

    """

    @classmethod
    def factory(cls, global_config, **local_config):
        """Used for paste app factories in paste.deploy config files.

        Any local configuration (that is, values under the [filter:APPNAME]
        section of the paste config) will be passed into the `__init__` method
        as kwargs.

        A hypothetical configuration would look like:

            [filter:analytics]
            redis_host = 127.0.0.1
            paste.filter_factory = nova.api.analytics:Analytics.factory

        which would result in a call to the `Analytics` class as

            import nova.api.analytics
            analytics.Analytics(app_from_paste, redis_host='127.0.0.1')

        You could of course re-implement the `factory` method in subclasses,
        but using the kwarg passing it shouldn't be necessary.

        """

        def _factory(app):
            return cls(app, **local_config)

        return _factory

    def __init__(self, application):
        self.application = application

    def process_request(self, req):
        """Called on each request.

        If this returns None, the next application down the stack will be
        executed. If it returns a response then that response will be returned
        and execution will stop here.

        """
        return None

    def process_response(self, response):
        """Do whatever you'd like to the response."""
        return response

    @webob.dec.wsgify(RequestClass=Request)
    def __call__(self, req):
        response = self.process_request(req)
        if response:
            return response
        response = req.get_response(self.application)
        return self.process_response(response)


class Debug(Middleware):
    """
    Techbk: copy from nova.api. This is good example for Middleware.
    Helper class for debugging a WSGI application.

    Can be inserted into any WSGI application chain to get information
    about the request and response.

    """

    @webob.dec.wsgify(RequestClass=Request)
    def __call__(self, req):
        print(('*' * 40) + ' REQUEST ENVIRON')
        for key, value in req.environ.items():
            print(key, '=', value)
        print()
        resp = req.get_response(self.application)

        print(('*' * 40) + ' RESPONSE HEADERS')
        for (key, value) in six.iteritems(resp.headers):
            print(key, '=', value)
        print()

        resp.app_iter = self.print_generator(resp.app_iter)

        return resp

    @staticmethod
    def print_generator(app_iter):
        """Iterator that prints the contents of a wrapper string."""
        print(('*' * 40) + ' BODY')
        for part in app_iter:
            sys.stdout.write(part)
            sys.stdout.flush()
            yield part
        print()


class JSONRequestDeserializer(object):
    def has_body(self, request):
        """
        Returns whether a Webob.Request object will possess an entity body.

        :param request:  Webob.Request object
        """
        if 'transfer-encoding' in request.headers:
            return True
        elif request.content_length > 0:
            return True

        return False

    def _sanitizer(self, obj):
        """Sanitizer method that will be passed to json.loads."""
        return obj

    def from_json(self, datastring):
        try:
            return json.loads(datastring, object_hook=self._sanitizer)
        except ValueError:
            msg = 'Malformed JSON in request body.'
            raise webob.exc.HTTPBadRequest(explanation=msg)

    def default(self, request):
        if self.has_body(request):
            return {'body': self.from_json(request.body)}
        else:
            return {}


class JSONResponseSerializer(object):
    def _sanitizer(self, obj):
        """Sanitizer method that will be passed to json.dumps."""
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return obj

    def to_json(self, data):
        return json.dumps(data, default=self._sanitizer)

    def default(self, response, result):
        response.content_type = 'application/json'
        response.body = self.to_json(result)

class Resource(object):
    def __init__(self, controller, deserializer=None, serializer=None):
        self.controller = controller
        self.serializer = serializer or JSONResponseSerializer()
        self.deserializer = deserializer or JSONRequestDeserializer()

    @webob.dec.wsgify(RequestClass=Request)
    def __call__(self, request):
        """WSGI method that controls (de)serialization and method dispatch."""
        action_args = self.get_action_args(request.environ)
        action = action_args.pop('action', None)

        deserialized_request_body = self.dispatch(self.deserializer,
                                             action, request)
        action_args.update(deserialized_request_body)

        action_result = self.dispatch(self.controller, action,
                                      request, **action_args)
        try:
            response = webob.Response(request=request)
            self.dispatch(self.serializer, action, response, action_result)
            return response

        except webob.exc.HTTPException as e:
            return e
        # return unserializable result (typically a webob exc)
        except Exception:
            return action_result

    def dispatch(self, obj, action, *args, **kwargs):
        """Find action-specific method on self and call it."""
        try:
            method = getattr(obj, action)
        except AttributeError:
            method = getattr(obj, 'default')

        return method(*args, **kwargs)

    def get_action_args(self, request_environment):
        """Parse dictionary created by routes library."""
        try:
            args = request_environment['wsgiorg.routing_args'][1].copy()
        except Exception:
            return {}

        try:
            del args['controller']
        except KeyError:
            pass

        try:
            del args['format']
        except KeyError:
            pass

        return args
from webob import Response
import webob.dec
from cal import wsgi

class ShowVersion(object):
    """
    Techbk: Copy from example.
    Show version....
    """

    def __init__(self, version):
        self.version = version

    def __call__(self, environ, start_response):
        res = Response()
        res.status = '200 OK'
        res.content_type = "text/plain"
        content = []
        content.append("%s\n" % self.version)
        res.body = '\n'.join(content)
        return res(environ, start_response)

    @classmethod
    def factory(cls, global_conf, **kwargs):
        print 'ShowVersion Middleware=)))'
        print "kwargs: ", kwargs
        return ShowVersion(kwargs['version'])



# class JsonMiddleware(Middleware):
#
#     def process_request(self, req):
#         body = JSONRequestDeserializer().default(req)
#         req.body = body
#         return req

    # def process_response(self, response):
    #     try:
    #         _response = webob.Response(request=request)
    #         JSONResponseSerializer.default( _response, response)
    #         return response
    #
    #     except webob.exc.HTTPException as e:
    #         return e
    #     # return unserializable result (typically a webob exc)
    #     except Exception:
    #         return {}

class BrokerMiddleware(wsgi.Middleware):

    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        body = wsgi.JSONRequestDeserializer().default(req)
        cloud = body.get('cloud')
        req.environ['cal.cloud'] = cloud
        return self.application

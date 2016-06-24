from webob import Response
import webob
from cal.wsgi import Middleware, JSONRequestDeserializer, JSONResponseSerializer

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



class JsonMiddleware(Middleware):

    def process_request(self, req):
        body = JSONRequestDeserializer.default(req.body)
        req.body = body
        return req

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

class BrokerMiddleware(Middleware):

    def process_request(self, req):
        cloud = req.body.get('cloud')
        req.body['cloud'] = cloud
        return req

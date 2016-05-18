from webob import Response

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
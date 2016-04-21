from cal import wsgi
from routes import Mapper

from .resource_extensions.basic import BasicController


class APIRouterV1(wsgi.Router):
    """
    Techbk:
    - Class nay co nhiem vu load extension Resource.
    - No khoi tao mot object Mapper
    """
    def __init__(self):
        mapper = Mapper()
        controller = BasicController()
        mapper.resource('basic', 'basics', controller=wsgi.Resource(controller))
        super(APIRouterV1, self).__init__(mapper)

    @classmethod
    def factory(cls, global_config, **local_conf):
        return cls()
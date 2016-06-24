from cal import wsgi
from routes import Mapper

from .resource_extensions.basic import Basics


class APIRouterV1(wsgi.Router):
    """
    Techbk:
    - Class nay co nhiem vu load extension Resource.
    - No khoi tao mot object Mapper
    """

    def __init__(self):
        mapper = Mapper()
        #Dang ky controller o day
        resources = [Basics(),]
        for resource in resources:
            mapper.resource(
                resource.member_name,
                resource.collection_name,
                controller=wsgi.Resource(resource.controller),
                member=resource.member,
                collection=resource.collection)

        super(APIRouterV1, self).__init__(mapper)

    @classmethod
    def factory(cls, global_config, **local_conf):
        return cls()
import cal.wsgi
from routes import Mapper

from cal.v1.resource_extensions.basic import Basics
import stevedore

class APIRouterV1(cal.wsgi.Router):
    """
    Techbk:
    - Class nay co nhiem vu load extension Resource.
    - No khoi tao mot object Mapper
    """

    @staticmethod
    def api_extension_namespace():
        return 'cal.v1.resource_extensions'

    def __init__(self):

        def _check_load_extension(ext):
            return True

        self.api_extension_manager = stevedore.enabled.EnabledExtensionManager(
            namespace=self.api_extension_namespace(),
            check_func=_check_load_extension,
            invoke_on_load=True
        )



        mapper = Mapper()
        # #Dang ky controller o day
        # resources = [Basics(),]
        for ext in self.api_extension_manager:
            resource = ext.obj
            mapper.resource(
                resource.member_name,
                resource.collection_name,
                controller=cal.wsgi.Resource(resource.controller),
                member=resource.member,
                collection=resource.collection)

        super(APIRouterV1, self).__init__(mapper)

    @classmethod
    def factory(cls, global_config, **local_conf):
        return cls()
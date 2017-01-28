"""BaseAbstract Class and BaseQuota Class for all object storage driver
   which we want to implement.
"""
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseDriver(object):
    """BaseAbstract Class for object storage driver"""

    def __init__(self, *args, **kwargs):
        super(BaseDriver, self).__init__()
        self.obj_storage_quota = BaseQuota()

    @abc.abstractmethod
    def create_container(self, container, **kwargs):
        pass

    @abc.abstractmethod
    def delete_container(self, container):
        pass

    @abc.abstractmethod
    def list_containers(self):
        pass

    @abc.abstractmethod
    def get_container(self, container):
        pass

    @abc.abstractmethod
    def update_container(self, container, **kwargs):
        pass

    @abc.abstractmethod
    def create_object(self, container, obj, contents,
                      content_length=None, **kwargs):
        pass

    @abc.abstractmethod
    def get_object(self, container, opj, **kwargs):
        pass

    @abc.abstractmethod
    def delete_object(self, container, obj, **kwargs):
        pass

    @abc.abstractmethod
    def list_container_objects(self, container):
        pass

    @abc.abstractmethod
    def update_object(self, container, obj, **kwargs):
        pass

    @abc.abstractmethod
    def copy_object(self, container, obj, **kwargs):
        pass


class BaseQuota(object):
    """docstring for QuotaObjectStorage"""

    def __init__(self):
        super(BaseQuota, self).__init__()

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseDriver(object):

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def create_network(self, name, *args, **kwargs):
        pass

    @abc.abstractmethod
    def delete_network(self, id):
        pass

    @abc.abstractmethod
    def list_network(self):
        pass

    @abc.abstractmethod
    def show_network(self, id):
        pass

    @abc.abstractmethod
    def update_network(self, id):
        pass

    @abc.abstractmethod
    def attach_to_router(self, id):
        pass

    @abc.abstractmethod
    def detach_to_router(self, id):
        pass

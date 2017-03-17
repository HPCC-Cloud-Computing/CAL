import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseDriver(object):
    """The base class that all Driver classes should inherit from."""

    def __init__(self):
        super(BaseDriver, self).__init__()

    @abc.abstractmethod
    def create_container(self, container, **kwargs):
        """Create container

        :param container(string): container name..
        :param **kwargs(dict): extend args for specific driver
        """
        pass

    @abc.abstractmethod
    def delete_container(self, container):
        """Delete container

        :param container: container name.
        """
        pass

    @abc.abstractmethod
    def list_containers(self):
        """List containers"""
        pass

    @abc.abstractmethod
    def stat_container(self, container):
        """Get container

        :param container: container name.
        """
        pass

    @abc.abstractmethod
    def update_container(self, container, metadata, **kwargs):
        """Update container

        :param container: container name.
        :param metadata(dict): additional metadata(headers)
                               to include in the request.
        :param **kwargs: extend args for specific driver.
        """
        pass

    @abc.abstractmethod
    def upload_object(self, container, obj, contents,
                      content_length=None, **kwargs):
        """Upload object

        :param container: container name.
        :param obj: object name.
        :param contents: a string, a file-like object or an iterable
                         to read object data from.
        :param content_length(int): size of the contents in bytes.
        :param **kwargs(dict): extend args for specific driver.
        """
        pass

    @abc.abstractmethod
    def download_object(self, container, obj, **kwargs):
        """Download object

        :param container: container name.
        :param obj: object name.
        :param **kwargs(dict): extend args for specific driver.
        """
        pass

    @abc.abstractmethod
    def stat_object(self, container, obj):
        """Stat object

        :params container: container name.
        :params object: object name.
        """
        pass

    @abc.abstractmethod
    def delete_object(self, container, obj, **kwargs):
        """Delete object

        :param container: container name.
        :param obj: object name.
        :param **kwargs
        """
        pass

    @abc.abstractmethod
    def list_container_objects(self, container, prefix=None, delimiter=None):
        """List container objects

        :param container: container name.
        :param prefix: prefix query
        :param delimiter: string to delimit the queries on
        """
        pass

    @abc.abstractmethod
    def update_object(self, container, obj, metadata, **kwargs):
        """Update object

        :param container(string): container name.
        :param obj: object name.
        :param metadata(dict): additional metadata(headers)
                               to include in the request.
        """
        pass

    @abc.abstractmethod
    def copy_object(self, container, obj, metadata=None,
                    destination=None, **kwargs):
        """Copy object

        :param container: destination container name.
        :param obj: destination object name.
        :param destination: The container and object name of the destination
                            object in the form of /container/object; if None,
                            the copy will use the source as the destination.
        :param metadata(dict): additional metadata(headers)
                               to include in the request
        :param **kwargs(dict): extend args for specific driver.
        """
        pass


class BaseQuota(object):
    """The base class that all Quota classes should inherit from."""

    def __init__(self):
        super(BaseQuota, self).__init__()

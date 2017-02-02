import calplus.conf
from calplus.base import BaseClient

CONF = calplus.conf.CONF


class Client(BaseClient):
    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""

    def __init__(self, provider, cloud_config, *args, **kwargs):
        BaseClient.__init__(self, CONF.object_storage.driver_path,
                            provider, cloud_config)

    def create_container(self, container, **kwargs):
        """Create container

        :param container(string): container name.
        :param **kwargs(dict): extend args for specific driver.
        """
        return self.driver.create_container(container, **kwargs)

    def delete_container(self, container):
        """Delete container

        :param container: container name.
        """
        return self.driver.delete_container(container)

    def list_containers(self):
        """List owned containers
        """
        return self.driver.list_container()

    def stat_container(self, container):
        """Stat container metadata

        :param container: container name.
        """
        return self.driver.stat_container(container)

    def update_container(self, container, headers, **kwargs):
        """Update container metadata

        :param container: container name.
        :param headers(dict): additional headers to include in the request.
        :param **kwargs(dict): extend args for specific driver.
        """
        return self.driver.update_container(container, **kwargs)

    def upload_object(self, container, obj, contents,
                      content_length=None, **kwargs):
        """Upload object

        :param container: container name.
        :param obj: object name.
        :param contents: object content.
        :param content_length(int): content length.
        :param **kwargs(dict): extend args for specific driver.
        """
        return self.driver.download_object(container, obj, contents=contents,
                                           content_length=content_length,
                                           **kwargs)

    def download_object(self, container, obj, **kwargs):
        """Download specific object

        :param container: container name.
        :param obj: object name.
        """
        return self.driver.download_object(container, obj, **kwargs)

    def stat_object(self, container, obj):
        """Stat object metadata

        :param container: container name.
        :param obj: object name.
        """
        return self.driver.stat_object(container, obj)

    def list_container_objects(self, container):
        """List container objects

        :param container: container name.
        """
        return self.driver.list_container_objects(container)

    def update_object(self, container, obj, headers, **kwargs):
        """Update object metadata

        :param container: container name.
        :param obj: object name.
        :param headers(dict): additional headers to include in the request.
        """
        return self.driver.update_object(container, obj, **kwargs)

    def copy_object(self, container, obj, **kwargs):
        """Copy object

        :param container: container name.
        :param obj: object name.
        """
        return self.driver.copy_object(container, obj, **kwargs)

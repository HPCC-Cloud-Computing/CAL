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

        :params container(string): container name.
        :params **kwargs(dict): extend args for specific driver.
        """
        return self.driver.create_container(container, **kwargs)

    def delete_container(self, container):
        """Delete container

        :params container: container name/container instance.
        """
        return self.driver.delete_container(container)

    def list_containers(self):
        """List owned containers
        """
        return self.driver.list_container()

    def get_container(self, container):
        """Get container data

        :params: container: container name/container instance.
        """
        return self.driver.get_container(container)

    def update_container(self, container, **kwargs):
        """Update container metadata

        :params: container: container name/container instance.
        :params: **kwargs(dict): extend args for specific driver.
        """
        return self.driver.update_container(container, **kwargs)

    def create_object(self, container, obj, contents,
                      content_length=None, **kwargs):
        """Create object

        :params: container: container name/container instance.
        :params: obj: object name.
        :params: content: object content.
        :params: content_length(int): content length.
        :params: **kwargs(dict): extend args for specific driver.
        """
        return self.driver.create_object(container, obj,
                                         contents, content_length, **kwargs)

    def get_object(self, container, obj, **kwargs):
        """Get specific object

        :params: container: container name/container instance.
        :params: obj: object name/object instance.
        """
        return self.driver.get_object(container, obj, **kwargs)

    def list_container_objects(self, container):
        """List container objects

        :params: container: container name/container instance.
        """
        return self.driver.list_container_objects(container)

    def update_object(self, container, obj, **kwargs):
        """Update object metadata

        :params: container: container name/container instance.
        :params: obj: object name/object instance.
        """
        return self.driver.update_object(container, obj, **kwargs)

    def copy_object(self, container, obj, **kwargs):
        """Copy object

        :params: container: container name/container instance.
        :params: obj: object name/object instance.
        """
        return self.driver.copy_object(container, obj, **kwargs)

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

    def list_containers(self):
        pass

    def create_container(self, container_name):
        pass

    def get_container(self, container_name):
        pass

    def delete_container(self, container):
        pass

    def list_container_objects(self, container):
        pass

    def get_object(self, container_name, object_name):
        pass

    def download_object(self, obj, destination_path, overwrite_existing=False,
                        delete_on_failure=True):
        pass

    def download_object_as_stream(self, obj, chunk_size=None):
        pass

    def upload_object(self, file_path, container, object_name, extra=None,
                      verify_hash=True, headers=None):
        pass

    def upload_object_via_stream(self, iterator, container,
                                 object_name, extra=None, headers=None):
        pass

    def delete_object(self, obj):
        pass


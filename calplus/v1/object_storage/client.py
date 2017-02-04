import logging
import calplus.conf

from calplus.base import BaseClient
from calplus.exceptions import DriverException

CONF = calplus.conf.CONF
LOG = logging.getLogger(__name__)


class Client(BaseClient):
    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""

    def __init__(self, provider, cloud_config):
        BaseClient.__init__(self, CONF.object_storage.driver_path,
                            provider, cloud_config)

    def create_container(self, container, **kwargs):
        """Create container

        :param container(string): container name.
        :param **kwargs(dict): extend args for specific driver.
        """
        try:
            LOG.debug('create_container() with %s is success.', self.driver)
            return self.driver.create_container(container, **kwargs)
        except DriverException as e:
            LOG.exception('create_container() with %s raised\
                            an exception %s.', self.driver, e)

    def delete_container(self, container):
        """Delete container

        :param container: container name.
        """
        try:
            LOG.debug('delete_container() with %s is success.', self.driver)
            return self.driver.delete_container(container)
        except DriverException as e:
            LOG.exception('delete_container() with %s raised\
                            an exception %s.', self.driver, e)

    def list_containers(self):
        """List owned containers
        """
        LOG.debug('list_buckets() with %s is success.', self.driver)
        return self.driver.list_container()

    def stat_container(self, container):
        """Stat container metadata

        :param container: container name.
        """
        LOG.debug('stat_container() with %s is success.', self.driver)
        return self.driver.stat_container(container)

    def update_container(self, container, headers, **kwargs):
        """Update container metadata

        :param container: container name.
        :param headers(dict): additional headers to include in the request.
        :param **kwargs(dict): extend args for specific driver.
        """
        LOG.debug('update_object() with %s is success.', self.driver)
        return self.driver.update_container(container, headers, **kwargs)

    def upload_object(self, container, obj, contents,
                      content_length=None, **kwargs):
        """Upload object

        :param container: container name.
        :param obj: object name.
        :param contents: object content.
        :param content_length(int): content length.
        :param **kwargs(dict): extend args for specific driver.
        """
        try:
            LOG.debug('upload_object() with %s is success.', self.driver)
            return self.driver.download_object(container, obj,
                                               contents=contents,
                                               content_length=content_length,
                                               **kwargs)
        except DriverException as e:
            LOG.exception('upload_object() with %s raised\
                            an exception %s.', self.driver, e)

    def download_object(self, container, obj, **kwargs):
        """Download specific object

        :param container: container name.
        :param obj: object name.
        """
        try:
            LOG.debug('download_object() with %s is success.', self.driver)
            return self.driver.download_object(container, obj, **kwargs)
        except DriverException as e:
            LOG.exception('download_object() with %s raised\
                            an exception %s.', self.driver, e)

    def stat_object(self, container, obj):
        """Stat object metadata

        :param container: container name.
        :param obj: object name.
        """
        LOG.debug('stat_object() with %s is success.', self.driver)
        return self.driver.stat_object(container, obj)

    def delete_object(self, container, obj, **kwargs):
        """Delete object in container

        :param container: container name.
        :param obj: obj name.
        """
        try:
            LOG.debug('delete_object() with %s is success.', self.driver)
            return self.driver.delete_object(container, obj, **kwargs)
        except DriverException as e:
            LOG.exception('download_object() with %s raised\
                            an exception %s.', self.driver, e)

    def list_container_objects(self, container):
        """List container objects

        :param container: container name.
        """
        LOG.debug('list_container_objects() with %s is success.', self.driver)
        return self.driver.list_container_objects(container)

    def update_object(self, container, obj, headers, **kwargs):
        """Update object metadata

        :param container: container name.
        :param obj: object name.
        :param headers(dict): additional headers to include in the request.
        """
        try:
            LOG.debug('update_object() with %s is success.', self.driver)
            return self.driver.update_object(container, obj, headers, **kwargs)
        except DriverException as e:
            LOG.exception('copy_object() with %s raised\
                            an exception %s.', self.driver, e)

    def copy_object(self, container, obj, **kwargs):
        """Copy object

        :param container: container name.
        :param obj: object name.
        """
        try:
            LOG.debug('copy_object() with %s is success.', self.driver)
            return self.driver.copy_object(container, obj, **kwargs)
        except DriverException as e:
            LOG.exception('copy_object() with %s raised\
                            an exception %s.', self.driver, e)

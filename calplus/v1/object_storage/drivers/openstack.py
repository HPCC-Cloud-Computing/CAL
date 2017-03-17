"""OpenStackDriver for Object Storage
   based on BaseDriver
"""

from keystoneauth1.identity import v3
from keystoneauth1 import session
from swiftclient.client import Connection

from calplus.v1.object_storage.drivers.base import BaseDriver, BaseQuota


PROVIDER = "OPENSTACK"


class OpenstackDriver(BaseDriver):
    """OpenStackDriver for Object Storage"""

    def __init__(self, cloud_config):
        super(OpenstackDriver, self).__init__()
        self.auth_url = cloud_config['os_auth_url']
        self.project_name = cloud_config['os_project_name']
        self.username = cloud_config['os_username']
        self.password = cloud_config['os_password']
        self.user_domain_name = \
            cloud_config.get('os_project_domain_name', 'default')
        self.project_domain_name = \
            cloud_config.get('os_user_domain_name', 'default')
        self.driver_name = \
            cloud_config.get('driver_name', 'default')
        self.tenant_id = cloud_config.get('tenant_id', None)
        self.limit = cloud_config.get('limit', None)
        self.auth_version = \
            cloud_config.get('os_auth_version', '2')
        self._setup()

    def _setup(self):
        auth = v3.Password(auth_url=self.auth_url,
                           user_domain_name=self.user_domain_name,
                           username=self.username,
                           password=self.password,
                           project_domain_name=self.project_domain_name,
                           project_name=self.project_name)
        sess = session.Session(auth=auth)
        self.client = Connection(auth_version=self.auth_version, session=sess)
        self.quota = OpenStackQuota(
            self.client, self.tenant_id, self.limit)

    def create_container(self, container, **kwargs):
        return self.client.put_container(container)

    def delete_container(self, container):
        return self.client.delete_container(container)

    def list_containers(self):
        return self.client.get_account()[1]

    def stat_container(self, container):
        return self.client.head_container(container)

    def update_container(self, container, metadata, **kwargs):
        metadata = {('x-container-meta-' + key.strip()): value
                    for key, value in metadata.items()
                    if not key.strip().startswith('x-container-meta-')}
        return self.client.post_container(container, metadata, **kwargs)

    def upload_object(self, container, obj, contents,
                      content_length=None, **kwargs):
        return self.client.put_object(container, obj, contents=contents,
                                      content_length=content_length, **kwargs)

    def download_object(self, container, obj, **kwargs):
        return self.client.get_object(container, obj, **kwargs)

    def stat_object(self, container, obj):
        return self.client.head_object(container, obj)

    def delete_object(self, container, obj, **kwargs):
        return self.client.delete_object(container, obj, **kwargs)

    def list_container_objects(self, container, prefix=None, delimiter=None):
        return self.client.get_container(container, prefix, delimiter)[1]

    def update_object(self, container, obj, metadata, **kwargs):
        # Format metedata key
        metadata = {('x-object-meta-' + key.strip()): value
                    for key, value in metadata.items()
                    if not key.strip().startswith('x-object-meta-')}
        return self.client.post_object(container, obj, metadata, **kwargs)

    def copy_object(self, container, obj, metadata=None,
                    destination=None, **kwargs):
        return self.client.copy_object(container, obj, headers=metadata,
                                       destination=destination, **kwargs)


class OpenStackQuota(BaseQuota):
    """OpenStackQuota"""

    def __init__(self, client, tenant_id=None, limit=None):
        super(OpenStackQuota, self).__init__()
        self.client = client
        self.tenant_id = tenant_id
        self.limit = limit
        self._setup()

    def _setup(self):
        pass

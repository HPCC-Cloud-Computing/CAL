""" OpenstackDriver for Compute
    based on BaseDriver
"""


from datetime import datetime

from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient.client import Client

from calplus.v1.compute.drivers.base import BaseDriver, BaseQuota


PROVIDER = "OPENSTACK"


class OpenstackDriver(BaseDriver):
    """docstring for OpenstackDriver"""

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
        self._setup()

    def _setup(self):
        auth = v3.Password(auth_url=self.auth_url,
                           user_domain_name=self.user_domain_name,
                           username=self.username,
                           password=self.password,
                           project_domain_name=self.project_domain_name,
                           project_name=self.project_name)
        sess = session.Session(auth=auth)
        self.client = Client("2.1", session=sess)
        self.quota = OpenstackQuota(
            self.client, self.tenant_id, self.limit)

    def create(self, image_id, flavor_id,
               network_id, name=None, number=1, **kargs):
        if name is None:
            name = unicode(datetime.now())
        server = self.client.servers.create(
            name=name,
            image=image_id,
            flavor=flavor_id,
            nics=[{'net-id': network_id}]
        )
        return server

    def show(self, instance_id):
        server = self.client.servers.get(
            instance_id
        )
        return server

    def list(self, **search_opts):
        servers = self.client.servers.list()
        return servers

    def delete(self, instance_id):
        self.client.servers.delete(instance_id)
        return True

    def shutdown(self, instance_id):
        self.client.servers.stop(instance_id)
        return True

    def start(self, instance_id):
        self.client.servers.start(instance_id)
        return True

    def reboot(self, instance_id):
        """Soft reboot"""
        self.client.servers.reboot(instance_id)
        return True

    def resize(self, instance_id, flavor_id):
        self.client.servers.resize(instance_id, flavor_id)
        self.client.servers.confirm_resize(instance_id)
        return True

    def add_sg(self, instance_id, new_sg):
        """Add a security group"""
        pass

    def delete_sg(self, instance_id, new_sg):
        """Delete a security group"""
        pass

    def list_sg(self, instance_id):
        """List all security group"""
        pass

    def add_nic(self, instance_id, new_sg):
        """Add a Network Interface Controller"""
        pass

    def delete_nic(self, instance_id, new_sg):
        """Delete a Network Interface Controller"""
        pass

    def list_nic(self, instance_id):
        """List all Network Interface Controller"""
        pass

    def add_private_ip(self, instance_id, new_sg):
        """Add private IP"""
        pass

    def delete_private_ip(self, instance_id, new_sg):
        """Delete private IP"""
        pass

    def add_public_ip(self, instance_id, new_sg):
        """Add a external IP"""
        pass

    def delete_public_ip(self, instance_id, new_sg):
        """Delete a external IP"""
        pass

    def list_ip(self, instance_id, new_sg):
        """Add all IPs"""
        pass


class OpenstackQuota(BaseQuota):
    """docstring for OpenStack Compute Quota"""
    def __init__(self, client, tenant_id=None, limit=None):
        super(OpenstackQuota, self).__init__()
        self.client = client
        self.tenant_id = tenant_id
        self.limit = limit
        self._setup()

    def _setup(self):
        pass

    def get_vcpus(self):
        pass

    def get_instances(self):
        pass

    def get_ram(self):
        pass

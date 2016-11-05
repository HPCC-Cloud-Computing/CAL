import calplus.conf
from calplus.base import BaseClient

CONF = calplus.conf.CONF


class Client(BaseClient):
    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""

    def __init__(self, provider, cloud_config, *args, **kwargs):
        BaseClient.__init__(self, CONF.compute.driver_path,
                            provider, cloud_config)

    def create(self, image, flavor,
               network_id, name, number, **kargs):
        return self.driver.create(image, flavor,
               network_id, name, number, **kargs)

    def show(self, instance_id):
        return self.driver.show(instance_id)

    def list(self, **search_opts):
        return self.driver.list(**search_opts)

    def delete(self, instance_id):
        return self.driver.delete(instance_id)

    def shutdown(self, instance_id):
        return self.driver.shutdown(instance_id)

    def start(self, instance_id):
        return self.driver.start(instance_id)

    def reboot(self, instance_id):
        return self.driver.reboot(instance_id)

    def resize(self, instance_id, configuration):
        pass

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

import cal.conf
from cal.lib.base import BaseClient

CONF = cal.conf.CONF


class Client(BaseClient):
    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""

    def __init__(self, provider, cloud_config, *args, **kwargs):
        BaseClient.__init__(self, CONF.network.driver_path,
                            provider, cloud_config)

    def create(self, name, cidr, **kwargs):
        self.driver.create(name, cidr, **kwargs)

    def delete(self, network_id):
        self.driver.delete(network_id)

    def list(self, **search_opts):
        self.driver.list(**search_opts)

    def show(self, subnet_id):
        self.driver.show(subnet_id)

    def update(self, network_id, network):
        self.driver.update(network_id, network)

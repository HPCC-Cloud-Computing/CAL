""" OpenstackDriver for Network
    based on NetworkDriver
"""

from neutronclient.v2_0 import client
from network_driver import NetworkDriver


class OpenstackNetWorkDriver(NetworkDriver):

    """docstring for OpenstackNetWorkDriver"""

    def __init__(self, auth_url, project_name,
                 username, password, **kargs):
        super(OpenstackNetWorkDriver, self).__init__()
        self.provider = "OPENSTACK"
        self.auth_url = auth_url
        self.project_name = project_name
        self.username = username
        self.password = password
        self.driver_name = kargs.pop('driver_name', 'default')
        self._setup()

    def _setup(self):
        self.client = client.Client(
            username=self.username,
            password=self.password,
            project_name=self.project_name,
            auth_url=self.auth_url
        )

    def create(self, network):
        return self.client.create_network({'network': network})

    def show(self, network_id):
        return self.client.show_network(network_id)

    def list(self, retrieve_all=True, **kargs):
        return self.client.list_networks(retrieve_all, **kargs)

    def update(self, network_id, network):
        return self.client.update_network(network_id, {'network': network})

    def delete(self, network_id):
        return self.client.delete_network(network_id)

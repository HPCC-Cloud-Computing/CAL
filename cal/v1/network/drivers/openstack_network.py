""" OpenstackDriver for Network
    based on NetworkDriver
"""

from neutronclient.v2_0 import client
from network_driver import NetworkDriver


class OpenstackNetWorkDriver(NetworkDriver):
    """docstring for OpenstackNetWorkDriver"""

    def __init__(self, auth_url, project_name,
                 username, password, user_domain_name=None,
                 project_domain_name=None, driver_name=None):
        super(OpenstackNetWorkDriver, self).__init__()
        self.provider = "OPENSTACK"
        self.auth_url = auth_url
        self.project_domain_name = project_domain_name
        self.user_domain_name = user_domain_name
        self.project_name = project_name
        self.username = username
        self.password = password
        if driver_name:
            self.driver_name = driver_name
        else:
            self.driver_name = "default"

        self._setup()

    def _setup(self):
        self.client = client.Client(
            username=self.username,
            password=self.password,
            tenant_name=self.project_name,
            auth_url=self.auth_url
        )

    def create(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

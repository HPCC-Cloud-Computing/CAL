""" OpenstackDriver for Network
    based on NetworkDriver
"""

from cal.tests import base
from neutronclient.v2_0 import client
#from network_driver import NetworkDriver

fake_config_driver = {
    'provider': 'OPENSTACK',
    'auth_url': 'http://controller:5000:v2_0',
    'username': 'test',
    'password': 'veryhard',
    'project_name': 'demo',
    'endpoint_url': 'http://controller:9696',
    'driver_name': 'default'
}


class OpenstackNetWorkDriverTest(base.TestCase):

    """docstring for OpenstackNetWorkDriver"""

    def setUp(self):
        super(OpenstackNetWorkDriverTest, self).setUp()
        self.provider = "OPENSTACK"
        self.auth_url = fake_config_driver['auth_url']
        self.project_name = fake_config_driver['project_name']
        self.username = fake_config_driver['username']
        self.password = fake_config_driver['password']
        self.endpoint_url = fake_config_driver['endpoint_url']
        self.driver_name = fake_config_driver['driver_name']
        self._setup()

    def _setup(self):
        self.client = client.Client(
            username=self.username,
            password=self.password,
            project_name=self.project_name,
            auth_url=self.auth_url,
            endpoint_url=self.endpoint_url
        )

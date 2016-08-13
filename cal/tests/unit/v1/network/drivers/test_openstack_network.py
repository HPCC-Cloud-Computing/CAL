""" OpenstackDriver for Network
    based on NetworkDriver
"""


import mock
from cal.tests import base
from keystoneauth1.identity import v3
from keystoneauth1 import session
from neutronclient.v2_0 import client
from network_driver import OpenstackNetWorkDriver, OpenstackNetworkQuota

fake_config_driver = {
    'provider': 'OPENSTACK',
    'auth_url': 'http://controller:5000:v2_0',
    'username': 'test',
    'password': 'veryhard',
    'project_name': 'demo',
    'endpoint_url': 'http://controller:9696',
    'driver_name': 'default',
    'project_domain_name': 'default',
    'user_domain_name': 'default'
}

fake_network_in = {'name': '',
                   'admin_state_up': admin_state_up}

fake_network_out = {'id': 'fake_id'}

fake_subnet_int = {"network_id": 'fake_id',
                   "ip_version": 'v4',
                   "cidr": 'fake_cidr',
                   "name": 'fake_name'}

fake_subnet_out = {'name': 'fake_name',
                   'description': None,
                   'id': 'fake_id',
                   'cidr': 'fake_cidr',
                   'cloud': 'OPENSTACK',
                   'gateway': 'fake_gateway_ip',
                   'security_group': None,
                   'allocation_pools': 'fake_name_allocation_pools',
                   'dns_nameservers': 'fake_dns_nameservers'
                   }


class OpenstackNetWorkDriverTest(base.TestCase):

    """docstring for OpenstackNetWorkDriver"""

    def setUp(self):
        super(OpenstackNetWorkDriverTest, self).setUp()
        self.provider = "OPENSTACK"
        auth = v3.Password(auth_url=fake_config_driver['auth_url'],
                           user_domain_name=fake_config_driver[
                               'user_domain_name'],
                           username=fake_config_driver['username'],
                           password=fake_config_driver['password'],
                           project_domain_name=fake_config_driver[
                               'project_domain_name'],
                           project_name=fake_config_driver['project_name'])
        sess = session.Session(auth=auth)
        self.client = client.Client(session=sess)

        self.fake_driver = OpenstackNetWorkDriver(self.client)
        self.fake_quota = OpenstackNetworkQuota(self.client)

    def test_create(self):
        self.mock_object(
            self.fake_driver, 'client.create_network',
            mock.Mock(return_value={'network': fake_network_out}))
        self.mock_object(
            self.fake_driver, 'client.create_subnet',
            mock.Mock(return_value={'subnet': fake_subnet_out}))

        self.fake_driver.create('fake_name', 'fake_cidr')

        self.fake_driver.client.create_network.assert_called_once_with(
            {'network': fake_network_in})
        self.fake_driver.client.create_subnet.assert_called_once_with(
            {'subnet': fake_subnet_int})

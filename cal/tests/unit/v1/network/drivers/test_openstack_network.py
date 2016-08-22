""" OpenstackDriver for Network
    based on NetworkDriver
"""


import mock
from cal.tests import base
from keystoneauth1.exceptions.base import ClientException
from cal.v1.network.drivers.openstack_network import OpenstackNetWorkDriver

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

fake_network_in = {
    'name': '',
    'admin_state_up': True
}

fake_network_out = {
    'id': 'fake_id'
}

fake_subnet_int = {
    "network_id": 'fake_id',
    "ip_version": 4,
    "cidr": 'fake_cidr',
    "name": 'fake_name'
}

fake_subnet_out = {
    'name': 'fake_name',
    'description': None,
    'id': 'fake_id',
    'cidr': 'fake_cidr',
    'cloud': 'OPENSTACK',
    'gateway_ip': 'fake_gateway_ip',
    'security_group': None,
    'allocation_pools': 'fake_name_allocation_pools',
    'dns_nameservers': 'fake_dns_nameservers'
}

fake_router = {
    'id': 'fake_router_id1'
}

fake_security_groups = {
    'id': 'fake_scg_id',
    'security_group_rules': []
}


class OpenstackNetWorkDriverTest(base.TestCase):

    """docstring for OpenstackNetWorkDriver"""

    def setUp(self):
        super(OpenstackNetWorkDriverTest, self).setUp()
        self.fake_driver = OpenstackNetWorkDriver(
            auth_url=fake_config_driver['auth_url'],
            project_name=fake_config_driver['project_name'],
            username=fake_config_driver['username'],
            password=fake_config_driver['password'],
            project_domain_name=fake_config_driver[
                'project_domain_name'],
            user_domain_name=fake_config_driver[
                'user_domain_name']
        )

    def test_create_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'create_network',
            mock.Mock(return_value={
                'network': fake_network_out
            }))
        self.mock_object(
            self.fake_driver.client, 'create_subnet',
            mock.Mock(return_value={
                'subnet': fake_subnet_out
            }))
        self.fake_driver.create('fake_name', 'fake_cidr')

        self.fake_driver.client.create_network.\
            assert_called_once_with({'network': fake_network_in})
        self.fake_driver.client.create_subnet.\
            assert_called_once_with({'subnet': fake_subnet_int})

    def test_create_unable_to_create_network(self):
        self.mock_object(
            self.fake_driver.client, 'create_network',
            mock.Mock(side_effect=ClientException))
        self.mock_object(
            self.fake_driver.client, 'create_subnet', mock.Mock())

        self.assertRaises(ClientException, self.fake_driver.create,
                          'fake_name', 'fake_cidr')

        self.fake_driver.client.create_network.\
            assert_called_once_with({'network': fake_network_in})
        self.assertFalse(self.fake_driver.client.create_subnet.called)

    def test_create_unable_to_create_subnet(self):
        self.mock_object(
            self.fake_driver.client, 'create_network',
            mock.Mock(return_value={
                'network': fake_network_out
            }))
        self.mock_object(
            self.fake_driver.client, 'create_subnet',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.create,
                          'fake_name', 'fake_cidr')

        self.fake_driver.client.create_network.\
            assert_called_once_with({'network': fake_network_in})
        self.fake_driver.client.create_subnet.\
            assert_called_once_with({'subnet': fake_subnet_int})

    def test_show_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'show_subnet',
            mock.Mock(return_value={
                'subnet': fake_subnet_out
            }))
        self.fake_driver.show('fake_id')

        self.fake_driver.client.show_subnet.\
            assert_called_once_with('fake_id')

    def test_show_unable_to_show_network(self):
        self.mock_object(
            self.fake_driver.client, 'show_subnet',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.show,
                          'fake_id')

        self.fake_driver.client.show_subnet.\
            assert_called_once_with('fake_id')

    def test_list_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'list_subnets',
            mock.Mock(return_value={
                'subnets': [fake_subnet_out]
            }))

        self.fake_driver.list()

        self.fake_driver.client.list_subnets.\
            assert_called_once_with()

    def test_list_unable_to_list_network(self):
        self.mock_object(
            self.fake_driver.client, 'list_subnets',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.list)

        self.fake_driver.client.list_subnets.\
            assert_called_once_with()

    def test_update_successfully(self):
        self.fake_driver.update('fake_id', fake_subnet_out)

    def test_update_unable_to_update_network(self):
        pass

    def test_delete_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'delete_network',
            mock.Mock(return_value=()))

        self.fake_driver.delete('fake_network_id')

        self.fake_driver.client.delete_network.\
            assert_called_once_with('fake_network_id')

    def test_delete_unable_to_detete_network(self):
        self.mock_object(
            self.fake_driver.client, 'delete_network',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.delete,
                          'fake_network_id')

        self.fake_driver.client.delete_network.\
            assert_called_once_with('fake_network_id')

    def test_get_networks(self):
        self.mock_object(
            self.fake_driver.client, 'list_subnets',
            mock.Mock(return_value={
                'subnets': [fake_subnet_out]
            }))

        self.fake_driver.network_quota.get_networks()

        self.fake_driver.client.list_subnets.\
            assert_called_once_with()

    def test_get_networks_unable_to_get_quota(self):
        self.mock_object(
            self.fake_driver.client, 'list_subnets',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_networks)

        self.fake_driver.client.list_subnets.\
            assert_called_once_with()

    def test_get_security_groups_quota(self):
        self.mock_object(
            self.fake_driver.client, 'get_quotas_tenant',
            mock.Mock(return_value={
                'tenant': {
                    'tenant_id': 'fake_tenant_id'
                }
            }))
        self.mock_object(
            self.fake_driver.client, 'list_security_groups',
            mock.Mock(return_value={
                'security_groups': [fake_security_groups]
            }))

        self.fake_driver.network_quota.get_security_groups()

        self.fake_driver.client.get_quotas_tenant.\
            assert_called_once_with()
        self.fake_driver.client.list_security_groups.\
            assert_called_once_with(tenant_id='fake_tenant_id')

    def test_get_security_groups_unable_to_get_tenant_id(self):
        self.mock_object(
            self.fake_driver.client, 'get_quotas_tenant',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_security_groups)

        self.fake_driver.client.get_quotas_tenant.\
            assert_called_once_with()

    def test_get_security_groups_unable_to_get_quota(self):
        self.mock_object(
            self.fake_driver.client, 'get_quotas_tenant',
            mock.Mock(return_value={
                'tenant': {
                    'tenant_id': 'fake_tenant_id'
                }
            }))
        self.mock_object(
            self.fake_driver.client, 'list_security_groups',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_security_groups)

        self.fake_driver.client.get_quotas_tenant.\
            assert_called_once_with()
        self.fake_driver.client.list_security_groups.\
            assert_called_once_with(tenant_id='fake_tenant_id')

    def test_get_floating_ips(self):
        self.mock_object(
            self.fake_driver.client, 'list_floatingips',
            mock.Mock(return_value={
                'floatingips': [
                    {'floating_ip_address': '192.168.50.238'},
                    {'floating_ip_address': '192.168.50.239'}
                ]
            }))

        self.fake_driver.network_quota.get_floating_ips()

        self.fake_driver.client.list_floatingips.\
            assert_called_once_with()

    def test_get_floating_ips_unable_to_get_quota(self):
        self.mock_object(
            self.fake_driver.client, 'list_floatingips',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_floating_ips)

        self.fake_driver.client.list_floatingips.\
            assert_called_once_with()

    def test_get_routers(self):
        self.mock_object(
            self.fake_driver.client, 'list_routers',
            mock.Mock(return_value={
                'routers': [fake_router]
            }))

        self.fake_driver.network_quota.get_routers()

        self.fake_driver.client.list_routers.\
            assert_called_once_with()

    def test_get_routers_unable_to_get_quota(self):
        self.mock_object(
            self.fake_driver.client, 'list_routers',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_routers)

        self.fake_driver.client.list_routers.\
            assert_called_once_with()

    def test_get_internet_gateways(self):
        self.fake_driver.network_quota.get_internet_gateways()

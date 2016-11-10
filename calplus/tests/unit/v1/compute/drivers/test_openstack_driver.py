""" OpenstackDriver for Compute
    based on BaseDriver fror Compute Resource
"""


import mock
from keystoneauth1.exceptions.base import ClientException

from calplus.tests import base
from calplus.v1.compute.drivers.openstack import OpenstackDriver

fake_config_driver = {
    'os_auth_url': 'http://controller:5000/v2_0',
    'os_username': 'test',
    'os_password': 'veryhard',
    'os_project_name': 'demo',
    'os_endpoint_url': 'http://controller:9696',
    'os_driver_name': 'default',
    'os_project_domain_name': 'default',
    'os_user_domain_name': 'default',
    'tenant_id': 'fake_tenant_id',
    'limit': {
        "subnet": 10,
        "network": 10,
        "floatingip": 50,
        "subnetpool": -1,
        "security_group_rule": 100,
        "security_group": 10,
        "router": 10,
        "rbac_policy": -1,
        "port": 50
    }
}


class OpenstackDriverTest(base.TestCase):

    """docstring for OpenstackDriverTest"""

    def setUp(self):
        super(OpenstackDriverTest, self).setUp()
        self.fake_driver = OpenstackDriver(fake_config_driver)

    def test_create_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'create',
            mock.Mock(return_value=mock.Mock))
        #NOTE: in fact: mock.Mock is novaclient.v2.servers.Server

        self.fake_driver.create(
            'fake_image_id',
            'fake_flavor_id',
            'fake_net_id',
            'fake_name'
        )

        self.fake_driver.client.servers.create.\
            assert_called_once_with(
                name='fake_name',
                image='fake_image_id',
                flavor='fake_flavor_id',
                nics=[{'net-id': 'fake_net_id'}]
            )

    def test_create_without_instance_name(self):
        self.mock_object(
            self.fake_driver.client.servers, 'create',
            mock.Mock(return_value=mock.Mock))
        # NOTE: in fact: mock.Mock is novaclient.v2.servers.Server

        self.fake_driver.create(
            'fake_image_id',
            'fake_flavor_id',
            'fake_net_id'
        )

        self.fake_driver.client.servers.create. \
            assert_called_once_with(
                name=mock.ANY,
                image='fake_image_id',
                flavor='fake_flavor_id',
                nics=[{'net-id': 'fake_net_id'}]
            )

    def test_create_unable_to_create_instance(self):
        self.mock_object(
            self.fake_driver.client.servers, 'create',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.create,
                'fake_image_id',
                'fake_flavor_id',
                'fake_net_id',
                'fake_name')

        self.fake_driver.client.servers.create. \
            assert_called_once_with(
                name='fake_name',
                image='fake_image_id',
                flavor='fake_flavor_id',
                nics=[{'net-id': 'fake_net_id'}]
            )

import mock
from oslo_config import cfg

import calplus.conf
from calplus import client
from calplus import exceptions
from calplus.tests.base import TestCase
from calplus.utils import pick_host_with_specific_provider
# from calplus.v1.network import client as network_client

CONF = calplus.conf.CONF


fake_aws_auth_opts = {
    'drive_name': 'New AMAZON',
    'type_driver': 'amazon',
    'aws_access_key_id': 'fake_id',
    'aws_secret_access_key': 'fake_key',
    'region_name': 'RegionOne',
    'endpoint_url': 'http://localhost:8788',
    'limit': {
        "subnet": 10,
        "vpc": 5,
        "floatingip": 50,
        "subnetpool": -1,
        "security_group_rule": 100,
        "security_group": 10,
        "router": 10,
        "rbac_policy": -1,
        "port": 50
    }
}


class TestClient(TestCase):

    @mock.patch.object(client, 'Client')
    def setUp(self, mock_client):
        super(TestClient, self).setUp()
        self.mock_client = mock_client

    def test_client_called_with_unsupported_provider(self):
        self.assertRaises(exceptions.ProviderNotFound, client.Client,
                          '1.0.0', 'compute', 'WrongProvider')

    def test_client_called_with_none_provider(self):
        test_client = client.Client(version='1.0.0', resource='network')
        self.assertIsNotNone(test_client.driver)

    def test_client_called_with_unsupported_version(self):
        self.assertRaises(exceptions.UnsupportedVersion, client.Client,
                          'wrong_version', 'compute', 'OpenStack')

    def test_client_called_with_none_resource(self):
        self.assertRaises(exceptions.ResourceNotDefined, client.Client,
                          '1.0.0', None, 'OpenStack')

    def test_client_called_with_unknow_resource(self):
        self.assertRaises(exceptions.ResourceNotFound, client.Client,
                          '1.0.0', 'wrong_resource', 'OpenStack')

    def test_client_called_with_not_found_host_of_provider(self):
        # I called directly bellow function because
        # We need a provider is neither ops nor aws
        host = pick_host_with_specific_provider('Other')
        self.assertIsNone(host)

    def test_client_called_with_cloud_config(self):
        test_client = client.Client(
            version='1.0.0',
            resource='network',
            provider='amazon',
            cloud_config=fake_aws_auth_opts
        )
        self.assertIsNotNone(test_client.driver)

    def test_client_called_realize_all_driver(self):
        def dict_to_opts_list(dict):
            """
            Convert cloud config to opts list
            :param dict:
            :return:
            """
            result = []
            keys = dict.keys()
            for key in keys:
                if isinstance(dict[key], str):
                    result.append(
                        cfg.StrOpt(key, default=dict[key])
                    )
                else:
                    result.append(
                        cfg.DictOpt(key, default=dict[key])
                    )
            return result

        # Add new aws host
        amazon_group2 = cfg.OptGroup('amazon2',
                                     title='Amazon Hosts')
        CONF.register_group(amazon_group2)
        list_opts = dict_to_opts_list(fake_aws_auth_opts)
        CONF.register_opts(list_opts, group=amazon_group2)

        enable_drivers = cfg.ListOpt(
            'enable_drivers',
            default=[
                'openstack',
                'amazon',
                amazon_group2.name
            ]
        )
        CONF.unregister_opt(cfg.ListOpt('enable_drivers'), 'providers')
        CONF.register_opt(enable_drivers, 'providers')

        #Test check list enable drivers
        enable_drivers = CONF.providers.enable_drivers
        expect_list = ['openstack', 'amazon', 'amazon2']
        trusty_list = []
        for driver in enable_drivers:
            if hasattr(CONF, driver):
                trusty_list.append(driver)
        self.assertTrue(len(expect_list and trusty_list) == 3)

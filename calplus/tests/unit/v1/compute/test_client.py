import mock
from keystoneauth1.exceptions.base import ClientException

from calplus.tests import base
from calplus.v1.compute import client


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
        "vcpus": 10,
        "instances": 10,
        "ram": 5000
    }
}


class ClientTest(base.TestCase):

    """docstring for ClientTest"""

    def setUp(self):
        super(ClientTest, self).setUp()
        self.fake_client = client.Client(
            'OpenStack', fake_config_driver)

    def test_create_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'create',
            mock.Mock(return_value="return object"))

        self.fake_client.create('1', '1',
                                'net_id', 'random', 1)

        self.fake_client.driver.create.\
            assert_called_once_with('1', '1',
                                    'net_id', 'random', 1)

    def test_create_unable_to_create(self):
        self.mock_object(
            self.fake_client.driver, 'create',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.create, '1', '1',
                          'net_id', 'random', 1)

        self.fake_client.driver.create.\
            assert_called_once_with('1', '1',
                                    'net_id', 'random', 1)

    def test_show_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'show',
            mock.Mock(return_value="return object"))

        self.fake_client.show('fake_id')

        self.fake_client.driver.show.\
            assert_called_once_with('fake_id')

    def test_show_unable_to_create(self):
        self.mock_object(
            self.fake_client.driver, 'show',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.show, 'fake_id')

        self.fake_client.driver.show.\
            assert_called_once_with('fake_id')

    def test_list_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'list',
            mock.Mock(return_value="list server objects"))

        self.fake_client.list()

        self.fake_client.driver.list.\
            assert_called_once_with()

    def test_list_unable_to_create(self):
        self.mock_object(
            self.fake_client.driver, 'list',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.list)

        self.fake_client.driver.list.\
            assert_called_once_with()

    def test_delete_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'delete',
            mock.Mock(return_value=True))

        self.fake_client.delete('fake_id')

        self.fake_client.driver.delete.\
            assert_called_once_with('fake_id')

    def test_delete_unable_to_create(self):
        self.mock_object(
            self.fake_client.driver, 'delete',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.delete, 'fake_id')

        self.fake_client.driver.delete.\
            assert_called_once_with('fake_id')

    def test_shutdown_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'shutdown',
            mock.Mock(return_value=True))

        self.fake_client.shutdown('fake_id')

        self.fake_client.driver.shutdown.\
            assert_called_once_with('fake_id')

    def test_shutdown_unable_to_create(self):
        self.mock_object(
            self.fake_client.driver, 'shutdown',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.shutdown, 'fake_id')

        self.fake_client.driver.shutdown.\
            assert_called_once_with('fake_id')

import mock

from calplus.exceptions import DriverException
from calplus.tests import base
from calplus.v1.object_storage import client


fake_config_driver = {
    'os_auth_url': 'http://controller:5000/v2_0',
    'os_username': 'test',
    'os_password': 'thisispassword',
    'os_project_name': 'admin',
    'os_endpoint_url': 'http://controller:9696',
    'os_driver_name': 'default',
    'os_project_domain_name': 'default',
    'os_user_domain_name': 'default',
    'tenant_id': 'admin_tenant_id',
}


class TestClient(base.TestCase):

    """Unittest for Object Storage Client"""

    def setUp(self):
        super(TestClient, self).setUp()
        self.fake_client = client.Client('OpenStack',
                                         fake_config_driver)

    def test_create_container_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'create_container',
            mock.Mock(return_value='return object')
        )

        self.fake_client.create_container('fake-container')
        self.fake_client.driver.create_container.\
            assert_called_once_with('fake-container')

    def test_create_container_failed(self):
        self.mock_object(
            self.fake_client,
            'create_container',
            mock.Mock(side_effect=DriverException())
        )
        self.assertRaises(DriverException,
                          self.fake_client.create_container,
                          'invalid-container')

    def test_delete_container_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'delete_container',
            mock.Mock(return_value='return object')
        )

        self.fake_client.delete_container('fake-container')
        self.fake_client.driver.delete_container.\
            assert_called_once_with('fake-container')

    def test_delete_container_failed(self):
        self.mock_object(
            self.fake_client,
            'delete_container',
            mock.Mock(side_effect=DriverException())
        )
        self.assertRaises(DriverException,
                          self.fake_client.delete_container,
                          'invalid-container')

    def test_stat_container_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'stat_container',
            mock.Mock(return_value='container\'s stat')
        )

        self.fake_client.stat_container('fake-container')
        self.fake_client.driver.stat_container.\
            assert_called_once_with('fake-container')

        def test_stat_container_failed(self):
            self.mock_object(
                self.fake_client,
                'stat_container',
                mock.Mock(side_effect=DriverException())
            )
            self.assertRaises(
                DriverException,
                self.fake_client.stat_container,
                'invalid-container'
            )

    def test_update_container_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'update_container',
            mock.Mock(return_value='container metadata is updated')
        )

        self.fake_client.update_container(
            'fake-container',
            {'newkey': 'newvalue'}
        )
        self.fake_client.driver.update_container.\
            assert_called_once_with(
                'fake-container',
                {'newkey': 'newvalue'}
            )

    def test_update_container_failed(self):
        self.mock_object(
            self.fake_client,
            'update_container',
            mock.Mock(side_effect=DriverException())
        )

        self.assertRaises(
            DriverException,
            self.fake_client.update_container,
            'invalid-container',
            {'newkey': 'newvalue'}
        )

    def test_upload_object_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'upload_object',
            mock.Mock(return_value='upload object successfully')
        )

        self.fake_client.upload_object('fake-container',
                                       'fake-obj',
                                       'Body',
                                       content_length=None)
        self.fake_client.driver.upload_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj',
                contents='Body',
                content_length=None
            )

    def test_upload_object_failed(self):
        self.mock_object(
            self.fake_client,
            'upload_object',
            mock.Mock(side_effect=DriverException())
        )

        self.assertRaises(
            DriverException,
            self.fake_client.upload_object,
            'invalid-container',
            'invalid-obj',
            'Body',
            content_length=None
        )

    def test_download_object_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'download_object',
            mock.Mock(return_value='download object successfully')
        )

        self.fake_client.download_object('fake-container',
                                         'fake-obj')
        self.fake_client.driver.download_object.\
            assert_called_once_with('fake-container',
                                    'fake-obj')

    def test_download_object_failed(self):
        self.mock_object(
            self.fake_client,
            'download_object',
            mock.Mock(side_effect=DriverException())
        )

        self.assertRaises(
            DriverException,
            self.fake_client.download_object,
            'invalid-container',
            'invalid-obj'
        )

    def test_stat_object_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'stat_object',
            mock.Mock(return_value='object\'s stat')
        )

        self.fake_client.stat_object(
            'fake-container',
            'fake-obj'
        )
        self.fake_client.driver.stat_object.\
            assert_called_once_with('fake-container',
                                    'fake-obj')

    def test_stat_object_failed(self):
        self.mock_object(
            self.fake_client,
            'stat_object',
            mock.Mock(side_effect=DriverException())
        )

        self.assertRaises(
            DriverException,
            self.fake_client.stat_object,
            'invalid-container',
            'invalid-obj'
        )

    def test_delete_object_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'delete_object',
            mock.Mock(return_value='delete successfully')
        )

        self.fake_client.delete_object('fake-container',
                                       'fake-obj')
        self.fake_client.driver.delete_object.\
            assert_called_once_with('fake-container',
                                    'fake-obj')

    def test_delete_object_failed(self):
        self.mock_object(
            self.fake_client,
            'delete_object',
            mock.Mock(side_effect=DriverException())
        )

        self.assertRaises(
            DriverException,
            self.fake_client.delete_object,
            'invalid-container',
            'invalid-obj'
        )

    def test_copy_object_in_same_container_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'copy_object',
            mock.Mock(return_value='copy successfully')
        )

        self.fake_client.copy_object('fake-container', 'fake-obj',
                                     metadata=None,
                                     destination='/fake-container/other-obj')
        self.fake_client.driver.copy_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj',
                metadata=None,
                destination='/fake-container/other-obj'
            )

    def test_copy_object_in_another_container_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'copy_object',
            mock.Mock(return_value='copy successfully')
        )

        self.fake_client.copy_object('fake-container', 'fake-obj',
                                     metadata=None,
                                     destination='/other-container/other-obj')
        self.fake_client.driver.copy_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj',
                metadata=None,
                destination='/other-container/other-obj'
            )

    def test_copy_object_failed(self):
        self.mock_object(
            self.fake_client,
            'copy_object',
            mock.Mock(side_effect=DriverException())
        )

        self.assertRaises(
            DriverException,
            self.fake_client.copy_object,
            'invalid-container',
            'invalid-obj',
            metadata=None,
            destination='/other-container/other-obj'
        )

    def test_update_object_successfully(self):
        self.mock_object(
            self.fake_client.driver,
            'update_object',
            mock.Mock(return_value='update object metadata successfully')
        )

        self.fake_client.update_object('fake-container',
                                       'fake-obj',
                                       {'newkey': 'newvalue'})
        self.fake_client.driver.update_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj',
                {'newkey': 'newvalue'}
            )

    def test_update_object_failed(self):
        self.mock_object(
            self.fake_client,
            'update_object',
            mock.Mock(side_effect=DriverException())
        )

        self.assertRaises(DriverException,
                          self.fake_client.update_object,
                          'invalid-container',
                          'invalid-obj',
                          {'newkey': 'newvalue'})

"""OpenstackDriver for ObjectStorage
based on BaseDriver for ObjectStorage Resource
"""


import mock

# from keystoneauth1.exceptions.base import ClientException
from swiftclient.exceptions import ClientException

from calplus.tests import base
from calplus.v1.object_storage.drivers.openstack import OpenstackDriver

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
    'os_auth_version': '2',
    'limit': {
    }
}

fake_stat_container_resp = {
    'content-length': '0',
    'x-container-object-count': '0',
    'accept-ranges': 'bytes',
    'x-storage-policy': 'Policy-0',
    'date': 'Tue, 21 Feb 2017 08:16:18 GMT',
    'x-timestamp': '1487664860.16448',
    'x-trans-id': 'tx4e0d357c5b944d0e95226-0058abf752',
    'x-container-bytes-used': '0',
    'content-type': 'text/plain; charset=utf-8'
}

fake_list_containers = [
    {
        'count': 5,
        'bytes': 10000,
        'name': 'fake-container-1'
    },
    {
        'count': 10,
        'bytes': 10000,
        'name': 'fake-container-2'
    }
]

# Object Hashing Value
fake_upload_object_resp = 'efdd72fff68e14ec242aab75647b9346'

fake_stat_object_resp = {
    'content-length': '122379',
    'accept-ranges': 'bytes',
    'last-modified': 'Tue, 21 Feb 2017 08:59:26 GMT',
    'etag': 'efdd72fff68e14ec242aab75647b9346',
    'x-timestamp': '1487667565.13697',
    'x-trans-id': 'tx8b6495117bd540c2910ce-0058ac0460',
    'date': 'Tue, 21 Feb 2017 09:12:00 GMT',
    'content-type': 'application/octet-stream'
}


class OpenStackDriverTest(base.TestCase):
    """Testing for OpenStackDriver"""

    def setUp(self):
        super(OpenStackDriverTest, self).setUp()
        self.fake_driver = OpenstackDriver(fake_config_driver)

    def test_create_container_successfully(self):
        self.mock_object(self.fake_driver.client, 'put_container',
                         mock.Mock(return_value=None))
        # NOTE: in fact, mock.Mock is swiftclient.client.Connection

        self.fake_driver.create_container('fake_container')
        self.fake_driver.client.put_container.assert_called_once_with(
            'fake_container')

    def test_create_container_failed_without_container_name_arg(self):
        self.assertRaises(
            TypeError, self.fake_driver.create_container)

    def test_delete_container_successfully(self):
        self.mock_object(self.fake_driver.client, 'delete_container',
                         mock.Mock(return_value=None))
        # NOTE: in fact, mock.Mock is swiftclient.client.Connection

        self.fake_driver.delete_container('fake_container')
        self.fake_driver.client.delete_container.assert_called_once_with(
            'fake_container')

    def test_delete_container_failed(self):
        self.mock_object(
            self.fake_driver.client,
            'delete_container',
            mock.Mock(side_effect=ClientException(
                'Container DELETE failed'
            ))
        )

        self.assertRaises(ClientException,
                          self.fake_driver.delete_container,
                          'invalid-container')
        self.fake_driver.client.delete_container.\
            assert_called_once_with('invalid-container')

    def test_stat_container_successfully(self):
        self.mock_object(self.fake_driver.client, 'head_container',
                         mock.Mock(return_value=fake_stat_container_resp))
        # NOTE: in fact, mock.Mock is swiftclient.client.Connection

        self.fake_driver.stat_container('fake_container')
        self.fake_driver.client.head_container.assert_called_once_with(
            'fake_container')

    def test_stat_container_failed(self):
        self.mock_object(
            self.fake_driver.client,
            'head_container',
            mock.Mock(side_effect=ClientException(
                'Container HEAD failed'
            ))
        )

        self.assertRaises(ClientException,
                          self.fake_driver.stat_container,
                          'invalid-container')
        self.fake_driver.client.head_container.\
            assert_called_once_with('invalid-container')

    def test_update_container_successfully(self):
        self.mock_object(
            self.fake_driver.client,
            'post_container',
            mock.Mock(return_value=None)
        )

        self.fake_driver.update_container('fake-container',
                                          {'newkey': 'newvalue'})
        self.fake_driver.client.post_container.\
            assert_called_once_with(
                'fake-container',
                {'x-container-meta-newkey': 'newvalue'}
            )

    def test_update_container_failed(self):
        self.mock_object(
            self.fake_driver.client,
            'post_container',
            mock.Mock(side_effect=ClientException(
                'Container POST failed'
            ))
        )

        self.assertRaises(ClientException,
                          self.fake_driver.update_container,
                          'invalid-container',
                          {'newkey': 'newvalue'})
        self.fake_driver.client.post_container.\
            assert_called_once_with(
                'invalid-container',
                {'x-container-meta-newkey': 'newvalue'}
            )

    def test_upload_object_successfully(self):
        self.mock_object(
            self.fake_driver.client,
            'put_object',
            mock.Mock(return_value=fake_upload_object_resp)
        )

        self.fake_driver.upload_object('fake-container',
                                       'fake-obj',
                                       'Body',
                                       content_length=None)
        self.fake_driver.client.put_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj',
                contents='Body',
                content_length=None
            )

    def test_upload_object_failed(self):
        self.mock_object(
            self.fake_driver.client,
            'put_object',
            mock.Mock(side_effect=ClientException(
                'Object PUT failed'
            ))
        )

        self.assertRaises(ClientException,
                          self.fake_driver.upload_object,
                          'invalid-container',
                          'invalid-obj',
                          'Body',
                          content_length=None)
        self.fake_driver.client.put_object.\
            assert_called_once_with(
                'invalid-container',
                'invalid-obj',
                contents='Body',
                content_length=None
            )

    def test_download_object_successfully(self):
        self.mock_object(
            self.fake_driver.client,
            'get_object',
            mock.Mock(return_value='fake-body')
        )

        self.fake_driver.download_object('fake-container',
                                         'fake-obj')
        self.fake_driver.client.get_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj'
            )

    def test_download_object_failed(self):
        self.mock_object(
            self.fake_driver.client,
            'get_object',
            mock.Mock(side_effect=ClientException(
                'Object GET failed'
            ))
        )

        self.assertRaises(ClientException,
                          self.fake_driver.download_object,
                          'invalid-container',
                          'invalid-obj')
        self.fake_driver.client.get_object.\
            assert_called_once_with(
                'invalid-container',
                'invalid-obj'
            )

    def test_stat_object_successfully(self):
        self.mock_object(
            self.fake_driver.client,
            'head_object',
            mock.Mock(return_value=fake_stat_object_resp)
        )

        self.fake_driver.stat_object('fake-container',
                                     'fake-obj')
        self.fake_driver.client.head_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj'
            )

    def test_stat_object_failed(self):
        self.mock_object(
            self.fake_driver.client,
            'head_object',
            mock.Mock(side_effect=ClientException(
                'Object HEAD failed'
            ))
        )

        self.assertRaises(ClientException,
                          self.fake_driver.stat_object,
                          'invalid-container',
                          'invalid-obj')
        self.fake_driver.client.head_object.\
            assert_called_once_with(
                'invalid-container',
                'invalid-obj'
            )

    def test_delete_object_successfully(self):
        self.mock_object(
            self.fake_driver.client,
            'delete_object',
            mock.Mock(return_value=None)
        )

        self.fake_driver.delete_object('fake-container',
                                       'fake-obj')
        self.fake_driver.client.delete_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj'
            )

    def test_delete_object_failed(self):
        self.mock_object(
            self.fake_driver.client,
            'delete_object',
            mock.Mock(side_effect=ClientException(
                'Object DELETE failed'
            ))
        )

        self.assertRaises(ClientException,
                          self.fake_driver.delete_object,
                          'invalid-container',
                          'invalid-obj')
        self.fake_driver.client.delete_object.\
            assert_called_once_with(
                'invalid-container',
                'invalid-obj'
            )

    def test_copy_object_in_same_container_successfully(self):
        self.mock_object(
            self.fake_driver.client,
            'copy_object',
            mock.Mock(return_value=None)
        )

        self.fake_driver.copy_object('fake-container', 'fake-obj',
                                     metadata=None,
                                     destination='/fake-container/other-obj')
        self.fake_driver.client.copy_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj',
                headers=None,
                destination='/fake-container/other-obj'
            )

    def test_copy_object_in_another_container_successfully(self):
        self.mock_object(
            self.fake_driver.client,
            'copy_object',
            mock.Mock(return_value=None)
        )

        self.fake_driver.copy_object('fake-container', 'fake-obj',
                                     metadata=None,
                                     destination='/other-container/other-obj')
        self.fake_driver.client.copy_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj',
                headers=None,
                destination='/other-container/other-obj'
            )

    def test_copy_object_failed(self):
        self.mock_object(
            self.fake_driver.client,
            'copy_object',
            mock.Mock(side_effect=ClientException(
                'Object COPY failed'
            ))
        )

        self.assertRaises(ClientException,
                          self.fake_driver.copy_object,
                          'invalid-container',
                          'invalid-obj',
                          metadata=None,
                          destination='/other-container/other-obj')
        self.fake_driver.client.copy_object.\
            assert_called_once_with(
                'invalid-container',
                'invalid-obj',
                headers=None,
                destination='/other-container/other-obj')

    def test_update_object_successfully(self):
        self.mock_object(
            self.fake_driver.client,
            'post_object',
            mock.Mock(return_value=None)
        )

        self.fake_driver.update_object('fake-container',
                                       'fake-obj',
                                       {'newkey': 'newvalue'})
        self.fake_driver.client.post_object.\
            assert_called_once_with(
                'fake-container',
                'fake-obj',
                {'x-object-meta-newkey': 'newvalue'}
            )

    def test_update_object_failed(self):
        self.mock_object(
            self.fake_driver.client,
            'post_object',
            mock.Mock(side_effect=ClientException(
                'Object POST failed'
            ))
        )

        self.assertRaises(ClientException,
                          self.fake_driver.update_object,
                          'invalid-container',
                          'invalid-obj',
                          {'newkey': 'newvalue'})
        self.fake_driver.client.post_object.\
            assert_called_once_with(
                'invalid-container',
                'invalid-obj',
                {'x-object-meta-newkey': 'newvalue'})

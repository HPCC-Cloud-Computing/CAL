""" AmazonDriver for ObjectStorage
    based on BaseDriver for ObjectStorage Resource
"""

import mock

from botocore.exceptions import ClientError

from calplus.tests import base
from calplus.tests import tools
from calplus.v1.object_storage.drivers.amazon import AmazonDriver


fake_config_driver = {
    'driver_name': 'fake_amazon',
    'aws_access_key_id': 'fake_id',
    'aws_secret_access_key': 'fake_key',
    'region_name': 'us-east-1',
    'endpoint_url': 'http://localhost:8788',
    'limit': {
    }
}

container_http_headers = {
    'content-length': '0',
    'x-amz-id-2': 'tx15e8f3835ce3430dae6ca-0058aab8a2',
    'x-amz-request-id': 'tx15e8f3835ce3430dae6ca-0058aab8a2',
    'location': '/fake-container',
    'x-trans-id': 'tx15e8f3835ce3430dae6ca-0058aab8a2',
    'date': 'Mon, 20 Feb 2017 09:36:35 GMT',
    'content-type': 'text/html; charset=UTF-8'
}

container_response_metadata = {
    'HTTPStatusCode': 200,
    'RetryAttempts': 0,
    'HostId': 'tx15e8f3835ce3430dae6ca-0058aab8a2',
    'RequestId': 'tx15e8f3835ce3430dae6ca-0058aab8a2',
    'HTTPHeaders': container_http_headers,
}


object_http_headers = {
    'content-length': '0',
    'x-amz-id-2': 'tx6d1f92e6591742adb5f7a-0058aabbde',
    'x-trans-id': 'tx6d1f92e6591742adb5f7a-0058aabbde',
    'last-modified': 'Mon, 20 Feb 2017 09:50:23 GMT',
    'etag': '"1447d7a0ff445c6e8367e1db1509e476"',
    'x-amz-request-id': 'tx6d1f92e6591742adb5f7a-0058aabbde',
    'date': 'Mon, 20 Feb 2017 09:50:23 GMT',
    'content-type': 'text/html; charset=UTF-8'
}

object_response_metadata = {
    'HTTPStatusCode': 200,
    'RetryAttempts': 0,
    'HostId': 'tx6d1f92e6591742adb5f7a-0058aabbde',
    'RequestId': 'tx6d1f92e6591742adb5f7a-0058aabbde',
    'HTTPHeaders': object_http_headers,
}

fake_create_container_resp = {
    'Location': '/fake-container',
    'ResponseMetadata': container_response_metadata
}

fake_list_containers_resp = {
    'Owner': {
        'DisplayName': 'admin:admin',
        'ID': 'admin:admin'
    },
    'Buckets': [
        {
            'CreationDate': 'fake-datetime',
            'Name': 'fake-container'
        },
        {
            'CreationDate': 'fake-datetime',
            'Name': 'fake-container-2'
        }
    ],
    'ResponseMetadata': container_response_metadata,
}

fake_stat_container_resp = {
    'ResponseMetadata': container_response_metadata
}

fake_upload_object_resp = {
    'ETag': '"1447d7a0ff445c6e8367e1db1509e476"',
    'ResponseMetadata': object_response_metadata,
}

fake_delete_container_resp = {
    'ResponseMetadata': tools.copy_and_update_dict(container_response_metadata,
                                                   {'HTTPStatusCode': 204})
}

fake_download_object_resp = {
    'Body': '<botocore.response.StreamingBody object at 0x7fa7072f8a50>',
    'ContentType': 'application/octet-stream',
    'ResponseMetadata': {
        'HTTPStatusCode': 200,
        'RetryAttempts': 0,
        'HostId': 'txeabc8f074b6142c6b3f01-0058aac1d7',
        'RequestId': 'txeabc8f074b6142c6b3f01-0058aac1d7',
        'HTTPHeaders': tools.copy_and_update_dict(object_http_headers, {
            'content-length': '3211953',
            'content-type': 'application/octet-stream'})
    },
    'LastModified': 'fake-datetime',
    'ContentLength': 3211953,
    'ETag': '"1447d7a0ff445c6e8367e1db1509e476"',
    'Metadata': {}
}

fake_stat_object_resp = {
    'ContentType': 'application/octet-stream',
    'ResponseMetadata': tools.copy_and_update_dict(
        object_response_metadata, {
            'HTTPHeaders': {
                'content-length': '3211953',
                'content-type': 'application/octet-stream'
            }
        }
    ),
    'LastModified': 'fake-datetime',
    'ContentLength': 3211953,
    'ETag': '"1447d7a0ff445c6e8367e1db1509e476"',
    'Metadata': {}
}

fake_delete_object_resp = fake_delete_container_resp.copy()

fake_list_container_objects_resp = {
    'Name': 'fake-container',
    'ResponseMetadata': tools.copy_and_update_dict(
        object_response_metadata, {
            'HTTPHeaders': {
                'content-length': '803',
                'content-type': 'application/xml'
            }
        }
    ),
    'MaxKeys': 1000,
    'Prefix': '',
    'Marker': '',
    'EncodingType': 'url',
    'IsTruncated': False,
    'Contents': [
        {
            'LastModified': 'fake-datetime',
            'ETag': '%22dccf4ddf639c627c9188f624b49da5ad%22',
            'StorageClass': 'STANDARD',
            'Key': '3.31.jpg',
            'Owner': {
                'DisplayName': 'admin:admin',
                'ID': 'admin:admin'
            },
            'Size': 6382610
        },
        {
            'LastModified': 'fake-datetime',
            'ETag': '%22d30e0c0c209f1e78303166a21fbad9ac%22',
            'StorageClass': 'STANDARD',
            'Key': '93-4.jpg',
            'Owner': {
                'DisplayName': 'admin:admin',
                'ID': 'admin:admin'
            },
            'Size': 628842
        }
    ]
}

fake_copy_object_resp = {
    'CopyObjectResult': {
        'LastModified': 'fake-datetime',
        'ETag': '"dccf4ddf639c627c9188f624b49da5ad"'
    },
    'ResponseMetadata': tools.copy_and_update_dict(
        object_response_metadata, {
            'HTTPHeaders': {
                'content-length': '803',
                'content-type': 'application/xml'
            }
        }
    ),
}

fake_error_code_resp = {
    'ResponseMetadata': {
        'HTTPStatusCode': 400,
        'RequestId': 'req-a4570d1a-8319-4d6f-8077-7044d72ef449',
        'HTTPHeaders': {
            'date': 'Sat, 24 Sep 2016 03:09:39 GMT',
            'content-length': '250',
            'content-type': 'text/xml'
        }
    },
    'Error': {
        'Message': "The specified bucket is not valid",
        'Code': 'InvalidBucketName'
    }
}


class AmazonDriverTest(base.TestCase):
    """Testing class for AmazonDriver"""

    def setUp(self):
        super(AmazonDriverTest, self).setUp()
        self.fake_driver = AmazonDriver(fake_config_driver)

    def test_create_container_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'create_bucket',
            mock.Mock(return_value=fake_create_container_resp)
        )

        self.fake_driver.create_container('fake-container')
        self.fake_driver.client.create_bucket.assert_called_once_with(
            Bucket='fake-container')

    def test_create_container_without_container_name_args(self):
        self.assertRaises(
            TypeError, self.fake_driver.create_container)

    def test_delete_container_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'delete_bucket',
            mock.Mock(return_value=fake_delete_container_resp)
        )

        self.fake_driver.delete_container('fake-container')
        self.fake_driver.client.delete_bucket.assert_called_once_with(
            Bucket='fake-container')

    def test_list_containers_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'list_buckets',
            mock.Mock(return_value=fake_list_containers_resp)
        )

        self.fake_driver.list_containers()
        self.fake_driver.client.list_buckets.assert_called_once_with()

    def test_list_containers_failed(self):
        self.mock_object(
            self.fake_driver.client, 'list_buckets',
            mock.Mock(side_effect=ClientError(
                fake_error_code_resp,
                'ListContainers'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.list_containers)
        self.fake_driver.client.list_buckets.assert_called_once_with()

    def test_stat_container_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'head_bucket',
            mock.Mock(return_value=fake_stat_container_resp)
        )

        self.fake_driver.stat_container('fake-container')
        self.fake_driver.client.head_bucket.assert_called_once_with(
            Bucket='fake-container')

    def test_stat_container_failed(self):
        self.mock_object(
            self.fake_driver.client, 'head_bucket',
            mock.Mock(side_effect=ClientError(
                fake_error_code_resp,
                'HeadContainer'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.stat_container,
                          'fake-container')
        self.fake_driver.client.head_bucket.assert_called_once_with(
            Bucket='fake-container')

    def test_upload_object_with_specific_contentlength_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'put_object',
            mock.Mock(return_value=fake_upload_object_resp)
        )

        self.fake_driver.upload_object('fake-container', 'fake-obj',
                                       'fake-content', 10)
        self.fake_driver.client.put_object.assert_called_once_with(
            Bucket='fake-container', Key='fake-obj',
            ContentLength=10, Body='fake-content')

    def test_upload_object_without_specific_contentlength_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'put_object',
            mock.Mock(return_value=fake_upload_object_resp)
        )

        self.fake_driver.upload_object('fake-container', 'fake-obj',
                                       'fake-content')
        self.fake_driver.client.put_object.assert_called_once_with(
            Bucket='fake-container', Key='fake-obj',
            ContentLength=None, Body='fake-content')

    def test_upload_object_failed(self):
        self.mock_object(
            self.fake_driver.client, 'put_object',
            mock.Mock(side_effect=ClientError(
                fake_error_code_resp,
                'UploadObject'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.upload_object,
                          'fake-container', 'fake-obj',
                          'fake-content')
        self.fake_driver.client.put_object.assert_called_once_with(
            Bucket='fake-container',
            Key='fake-obj',
            ContentLength=None,
            Body='fake-content'
        )

    def test_download_object_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'get_object',
            mock.Mock(return_value=fake_download_object_resp)
        )

        self.fake_driver.download_object('fake-container', 'fake-obj')
        self.fake_driver.client.get_object.assert_called_once_with(
            Bucket='fake-container',
            Key='fake-obj'
        )

    def test_download_object_failed(self):
        self.mock_object(
            self.fake_driver.client, 'get_object',
            mock.Mock(side_effect=ClientError(
                fake_error_code_resp,
                'DownloadObject'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.download_object,
                          'fake-container', 'fake-obj')
        self.fake_driver.client.get_object.assert_called_once_with(
            Bucket='fake-container',
            Key='fake-obj',
        )

    def test_stat_object_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'head_object',
            mock.Mock(return_value=fake_stat_object_resp)
        )

        self.fake_driver.stat_object('fake-container', 'fake-obj')
        self.fake_driver.client.head_object.assert_called_once_with(
            Bucket='fake-container',
            Key='fake-obj'
        )

    def test_stat_object_failed(self):
        self.mock_object(
            self.fake_driver.client, 'head_object',
            mock.Mock(side_effect=ClientError(
                fake_error_code_resp,
                'HeadObject'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.stat_object,
                          'fake-container', 'fake-obj')
        self.fake_driver.client.head_object.assert_called_once_with(
            Bucket='fake-container',
            Key='fake-obj',
        )

    def test_delete_object_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'delete_object',
            mock.Mock(return_value=fake_delete_object_resp)
        )

        self.fake_driver.delete_object('fake-container', 'fake-obj')
        self.fake_driver.client.delete_object.assert_called_once_with(
            Bucket='fake-container',
            Key='fake-obj'
        )

    def test_delete_object_failed(self):
        self.mock_object(
            self.fake_driver.client, 'delete_object',
            mock.Mock(side_effect=ClientError(
                fake_error_code_resp,
                'DeleteObject'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.delete_object,
                          'fake-container', 'fake-obj')
        self.fake_driver.client.delete_object.assert_called_once_with(
            Bucket='fake-container',
            Key='fake-obj',
        )

    def test_list_container_objects_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'list_objects',
            mock.Mock(return_value=fake_list_container_objects_resp)
        )

        self.fake_driver.list_container_objects('fake-container',
                                                prefix=None, delimiter=None)
        self.fake_driver.client.list_objects.assert_called_once_with(
            Bucket='fake-container',
            Prefix=None,
            Delimiter=None,
        )

    def test_list_container_objects_failed(self):
        self.mock_object(
            self.fake_driver.client, 'list_objects',
            mock.Mock(side_effect=ClientError(
                fake_error_code_resp,
                'ListObjects'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.list_container_objects,
                          'fake-container',
                          prefix=None,
                          delimiter=None)
        self.fake_driver.client.list_objects.assert_called_once_with(
            Bucket='fake-container',
            Prefix=None,
            Delimiter=None,
        )

    def test_copy_object_in_same_container_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'copy_object',
            mock.Mock(return_value=fake_copy_object_resp)
        )

        self.fake_driver.copy_object(
            'fake-container', 'fake-obj',
            metadata=None,
            destination='/fake-container/fake-copy-obj')
        self.fake_driver.client.copy_object.assert_called_once_with(
            Bucket='fake-container',
            Key='fake-copy-obj',
            Metadata={},
            MetadataDirective='COPY',
            CopySource={
                'Bucket': 'fake-container',
                'Key': 'fake-obj'
            }
        )

    def test_copy_object_in_another_container_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'copy_object',
            mock.Mock(return_value=fake_copy_object_resp)
        )

        self.fake_driver.copy_object(
            'fake-container', 'fake-obj',
            metadata=None,
            destination='/another-fake-container/fake-copy-obj')
        self.fake_driver.client.copy_object.assert_called_once_with(
            Bucket='another-fake-container',
            Key='fake-copy-obj',
            Metadata={},
            MetadataDirective='COPY',
            CopySource={
                'Bucket': 'fake-container',
                'Key': 'fake-obj'
            }
        )

    def test_copy_object_failed(self):
        self.mock_object(
            self.fake_driver.client, 'copy_object',
            mock.Mock(side_effect=ClientError(
                fake_error_code_resp,
                'CopyObject'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.copy_object,
                          'fake-container',
                          'fake-obj',
                          metadata=None,
                          destination='/fake-container/fake-copy-obj')
        self.fake_driver.client.copy_object.assert_called_once_with(
            Bucket='fake-container',
            Key='fake-copy-obj',
            Metadata={},
            MetadataDirective='COPY',
            CopySource={
                'Bucket': 'fake-container',
                'Key': 'fake-obj'
            }
        )

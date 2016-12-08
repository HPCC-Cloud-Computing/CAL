""" AmazonDriver for Compute
    based on BaseDriver for Compute Resource
"""


import mock

from botocore.exceptions import ClientError

from calplus.tests import base
from calplus.v1.compute.drivers.amazon import AmazonDriver


fake_config_driver = {
    'driver_name': 'AMAZON1',
    'aws_access_key_id': 'fake_id',
    'aws_secret_access_key': 'fake_key',
    'region_name': 'us-east-1',
    'endpoint_url': 'http://localhost:8788',
    'limit': {
    }
}

fake_error_code = {
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
        'Message': "The subnet ID 'fake_id' does not exist",
        'Code': 'InvalidSubnetID.NotFound'
    }
}


class AmazonDriverTest(base.TestCase):

    """docstring for AmazonDriverTest"""

    def setUp(self):
        super(AmazonDriverTest, self).setUp()
        self.fake_driver = AmazonDriver(fake_config_driver)

    def test_create_successfully(self):
        self.mock_object(
            self.fake_driver.resource, 'create_instances',
            mock.Mock(return_value=mock.Mock))

        self.fake_driver.create(
            'fake_image_id',
            'fake_flavor_id',
            'fake_net_id',
            'fake_name'
        )

        self.fake_driver.resource.create_instances.\
            assert_called_once_with(
                ImageId='fake_image_id',
                MinCount=1,
                MaxCount=1,
                InstanceType='fake_flavor_id',
                SubnetId='fake_net_id',
                IamInstanceProfile={
                    'Arn': '',
                    'Name': 'fake_name'
                }
            )

    def test_create_without_instance_name(self):
        self.mock_object(
            self.fake_driver.resource, 'create_instances',
            mock.Mock(return_value=mock.Mock))

        self.fake_driver.create(
            'fake_image_id',
            'fake_flavor_id',
            'fake_net_id'
        )

        self.fake_driver.resource.create_instances. \
            assert_called_once_with(
                ImageId='fake_image_id',
                MinCount=1,
                MaxCount=1,
                InstanceType='fake_flavor_id',
                SubnetId='fake_net_id',
                IamInstanceProfile={
                    'Arn': '',
                    'Name': mock.ANY
                }
            )

    def test_create_unable_to_create_instance(self):
        self.mock_object(
            self.fake_driver.resource, 'create_instances',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            ))
        )

        self.assertRaises(ClientError, self.fake_driver.create,
                'fake_image_id',
                'fake_flavor_id',
                'fake_net_id',
                'fake_name')

        self.fake_driver.resource.create_instances. \
            assert_called_once_with(
                ImageId='fake_image_id',
                MinCount=1,
                MaxCount=1,
                InstanceType='fake_flavor_id',
                SubnetId='fake_net_id',
                IamInstanceProfile={
                    'Arn': '',
                    'Name': mock.ANY
                }
            )

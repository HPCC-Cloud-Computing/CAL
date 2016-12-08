""" OpenstackDriver for Compute
    based on BaseDriver
"""


from datetime import datetime
import six

import boto3

from calplus.v1.compute.drivers.base import BaseDriver, BaseQuota


PROVIDER = "AMAZON"


class AmazonDriver(BaseDriver):
    """docstring for AmazonDriver"""

    def __init__(self, cloud_config):
        super(AmazonDriver, self).__init__()
        self.aws_access_key_id = cloud_config['aws_access_key_id']
        self.aws_secret_access_key = cloud_config['aws_secret_access_key']
        self.endpoint_url = cloud_config['endpoint_url']
        self.region_name = cloud_config.get('region_name', None)
        self.driver_name = \
            cloud_config.get('driver_name', 'default')
        self.limit = cloud_config.get('limit', None)
        self._setup()

    def _setup(self):
        parameters = {
            'aws_access_key_id': self.aws_access_key_id,
            'aws_secret_access_key': self.aws_secret_access_key,
            'region_name': self.region_name,
            'endpoint_url': self.endpoint_url
        }
        self.resource = boto3.resource('ec2', **parameters)
        self.client = boto3.client('ec2', **parameters)
        self.quota = AmazonQuota(self.client, self.limit)

    def create(self, image_id, flavor_id,
               network_id, name=None, number=1, **kargs):
        if name is None:
            name = six.text_type(datetime.now())
        profile = {
            'Arn': '',
            'Name': name
        }
        server = self.resource.create_instances(
            ImageId=image_id,
            MinCount=number,
            MaxCount=number,
            InstanceType=flavor_id,
            SubnetId=network_id,
            IamInstanceProfile=profile
        )
        return server

    def show(self, instance_id):
        servers = self.client.describe_instances(InstanceIds=[instance_id])
        return servers.get("Reservations")[0].get("Instances")[0]

    def list(self, **search_opts):
        pass

    def delete(self, instance_id):
        pass

    def shutdown(self, instance_id):
        pass

    def start(self, instance_id):
        pass

    def reboot(self, instance_id):
        pass

    def resize(self, instance_id, configuration):
        pass

    def add_sg(self, instance_id, new_sg):
        """Add a security group"""
        pass

    def delete_sg(self, instance_id, new_sg):
        """Delete a security group"""
        pass

    def list_sg(self, instance_id):
        """List all security group"""
        pass

    def add_nic(self, instance_id, net_id):
        pass

    def delete_nic(self, instance_id, AttachmentId):
        pass

    def list_nic(self, instance_id):
        pass

    def add_private_ip(self):
        """Add private IP"""
        pass

    def delete_private_ip(self):
        """Delete private IP"""
        pass

    def associate_public_ip(self, instance_id, public_ip_id, private_ip=None):
        """Associate a external IP"""
        pass

    def disassociate_public_ip(self, public_ip_id):
        """Disassociate a external IP"""
        pass

    def list_ip(self, instance_id):
        pass


class AmazonQuota(BaseQuota):

    """docstring for AmazonQuota"""

    def __init__(self, client, limit=None):
        super(AmazonQuota, self).__init__()
        self.client = client
        self.limit = limit
        self._setup()

    def _setup(self):
        pass

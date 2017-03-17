import boto3

from calplus.v1.object_storage.drivers.base import BaseDriver, BaseQuota


PROVIDER = 'AMAZON'


class AmazonDriver(BaseDriver):
    """AmazonDriver for Object Storage"""

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

        self.client = boto3.client('s3', **parameters)
        self.quota = AmazonQuota(self.client, self.limit)

    def create_container(self, container, **kwargs):
        return self.client.create_bucket(Bucket=container, **kwargs)

    def delete_container(self, container):
        return self.client.delete_bucket(Bucket=container)

    def list_containers(self):
        return self.client.list_buckets()

    def stat_container(self, container):
        return self.client.head_bucket(Bucket=container)

    def update_container(self, container, headers, **kwargs):
        pass

    def upload_object(self, container, obj, contents,
                      content_length=None, **kwargs):
        return self.client.put_object(Bucket=container, Key=obj,
                                      ContentLength=content_length,
                                      Body=contents)

    def download_object(self, container, obj, **kwargs):
        return self.client.get_object(Bucket=container, Key=obj)

    def stat_object(self, container, obj):
        return self.client.head_object(Bucket=container, Key=obj)

    def delete_object(self, container, obj, **kwargs):
        return self.client.delete_object(Bucket=container, Key=obj,
                                         **kwargs)

    def list_container_objects(self, container, prefix=None, delimiter=None):
        return self.client.list_objects(Bucket=container, Prefix=prefix,
                                        Delimiter=delimiter)

    def update_object(self, container, obj, metadata=None, **kwargs):
        # Format metadata key, because metadata key/name must
        # begin with 'x-amz-'
        metadata = {('x-amz-' + key.strip()).lower(): value
                    for key, value in metadata.items()
                    if key.strip().startswith('x-amz-')}
        # Becasuse After you upload the object, you cannot
        # modify object metadata. The only way to modify object
        # metadata is to make a copy of the object and set the metadata.
        _old_metadata = self.stat_object(container, obj)
        destination = '/' + container + '/' + obj
        _new_metadata = _old_metadata.update(metadata)
        return self.copy_object(container, obj, metadata=_new_metadata,
                                destination=destination, **kwargs)

    def copy_object(self, container, obj, metadata=None,
                    destination=None, **kwargs):
        copysource = {
            'Bucket': container,
            'Key': obj
        }

        if destination:
            metadata_directive = 'COPY'
            dst_container, dst_obj = destination.strip('/').split('/')
        else:
            metadata_directive = 'REPLACE'
            dst_container, dst_obj = container, obj
        if not metadata:
            metadata = {}
        return self.client.copy_object(Bucket=dst_container, Key=dst_obj,
                                       Metadata=metadata,
                                       MetadataDirective=metadata_directive,
                                       CopySource=copysource)


class AmazonQuota(BaseQuota):
    """AmazonQuota for ObjectStorage"""

    def __init__(self, client, limit=None):
        super(AmazonQuota, self).__init__()
        self.client = client
        self.limit = limit
        self._setup()

    def _setup(self):
        pass

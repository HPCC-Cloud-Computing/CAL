""" OpenstackDriver for Block Storage
    based on BaseDriver
"""

from keystoneauth1.identity import v3
from keystoneauth1 import session
from cinderclient.client import Client

from calplus.v1.block_storage.drivers.base import BaseDriver, BaseQuota


class OpenstackDriver(BaseDriver):

    def __init__(self, cloud_config):
        super(OpenstackDriver, self).__init__()
        self.auth_url = cloud_config['os_auth_url']
        self.project_name = cloud_config['os_project_name']
        self.username = cloud_config['os_username']
        self.password = cloud_config['os_password']
        self.user_domain_name = cloud_config.get('os_user_domain_name',
                                                 'default')
        self.project_domain_name = cloud_config.get('os_project_domain_name',
                                                    'default')
        self.driver_name = cloud_config.get('driver_name', 'default')
        self.tenant_id = cloud_config.get('tenant_id', None)
        self.limit = cloud_config.get('limit', None)
        self.client_version = cloud_config.get('os_cinder)_client',
                                               '2')
        self._setup()

    def _setup(self):
        auth = v3.Password(auth_url=self.auth_url,
                           user_domain_name=self.user_domain_name,
                           username=self.username,
                           password=self.password,
                           project_domain_name=self.project_domain_name,
                           project_name=self.project_name)

        _session = session.Session(auth=auth)
        self.client = Client(self.client_version, session=_session)
        self.volumes = self.client.volumes
        self.block_storage_quota = OpenstackQuota(self.client,
                                                  self.tenant_id,
                                                  self.limit)

    def create(self, size, volume_type, **kwargs):
        """Create a volume

        :param size: Size of volume in GB
        :param volume_type: Type of volume
        :param **kwargs: Arbitrary keyword arguments.
        """
        return self.volumes.create(
            size=size,
            volume_type=volume_type,
            **kwargs
        )

    def get(self, volume_id):
        """Get a volume.

        :param volume_id: The ID of the volume to get.
        """
        return self.volumes.get(volume_id)

    def list(self, **kwargs):
        """Lists all volumes.

        :param **kwargs: Arbitrary keyword arguments.
        """
        return self.volumes.list(**kwargs)

    def delete(self, volume_id):
        """Delete a volume.

        :param volume_id: Id of the volume to delete.
        """
        return self.volumes.delete(volume_id)

    def update(self, volume_id, **kwargs):
        """Update the name or description for a volume.

        :params volume_id: Id of the volume to update.
        :param **kwargs: Arbitrary keyword arguments.
        """
        return self.volumes.update(volume_id, **kwargs)

    def attach(self, volume_id, instance_uuid):
        """Set attachment metadata.

        :params volume_id: Id of the volume to update.
        :param instance_uuid: uuid of the attaching instance.
        """
        return self.volumes.attach(volume_id, instance_uuid)

    def detach(self, volume_id, attachment_uuid):
        """Clear attachment metadata.

        :params volume_id: Id of the volume to update.
        :param attachment_uuid: The uuid of the volume attachment.
        """
        return self.volumes.detach(volume_id, attachment_uuid)


class OpenstackQuota(BaseQuota):

    def __init__(self, client, tenant_id=None,
                 absolute_limits=None, rate_limits=None):
        super(OpenstackQuota, self).__init__()
        self.client = client
        self.tenant_id = tenant_id
        self.absolute_limits = absolute_limits
        # self.rate_limits = rate_limits
        self._setup()

    def _setup(self):
        if not self.tenant_id:
            self.tenant_id = self.client.quotas.resource_class.id

        if not self.absolute_limits:
            self.absolute_limits = {}
            for a_limit in self.client.limits.get().absolute:
                self.absolute_limits[str(a_limit.name)] = a_limit.value
        # if not self.rate_limits:
        #     self.rate_limits = list(cli.limits.get().rate)

    def get_volumes(self):
        volumes = {
            'max': self.absolute_limits['maxTotalVolumes'],
            'used': self.absolute_limits['totalVolumesUsed']
        }

        return volumes

    def get_snapshots(self):
        snapshots = {
            'max': self.absolute_limits['maxTotalSnapshots'],
            'used': self.absolute_limits['totalSnapshotsUsed']
        }

        return snapshots

    def get_backups(self):
        backups = {
            'max': self.absolute_limits['maxTotalBackups'],
            'used': self.absolute_limits['totalBackupsUsed']
        }

        return backups

    def get_volume_gigabytes(self):
        volume_gigabytes = {
            'max': self.absolute_limits['maxTotalVolumeGigabytes'],
            'used': self.absolute_limits['totalGigabytesUsed']
        }

        return volume_gigabytes

    def get_backup_gigabytes(self):
        backup_gigabytes = {
            'max': self.absolute_limits['maxTotalBackupGigabytes'],
            'used': self.absolute_limits['totalBackupGigabytesUsed']
        }

        return backup_gigabytes

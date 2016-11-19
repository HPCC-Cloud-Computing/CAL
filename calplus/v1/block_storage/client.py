import calplus.conf
from calplus.base import BaseClient

CONF = calplus.conf.CONF


class Client(BaseClient):

    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""

    def __init__(self, provider, cloud_config, *args, **kwargs):
        BaseClient.__init__(self, CONF.block_storage.driver_path,
                            provider, cloud_config)

    def create(self, size, volume_type, **kwargs):
        """Create a volume.

        :param size: Size of volume in GB.
        :param volume_type: Type of volume.
        :param **kwargs: Arbitrary keyword arguments.
        """
        return self.driver.create(size, volume_type, **kwargs)

    def list(self, **kwargs):
        """List all volumes.

        :param **kwargs: Arbitrary keyword arguments.
        """
        return self.driver.list(**kwargs)

    def get(self, volume_id):
        """Get a volume.

        :param volume_id: The ID of the volume to get.
        """
        return self.driver.get(volume_id)

    def delete(self, volume_id):
        """Delete a volume.

        :param volume_id: Id of the volume to delete.
        """
        return self.driver.delete(volume_id)

    def update(self, volume_id, **kwargs):
        """Update the name or description for a volume.

        :params volume_id: Id of the volume to update.
        :param **kwargs: Arbitrary keyword arguments.
        """
        return self.driver.update(volume_id, **kwargs)

    def attach(self, volume_id, instance_uuid):
        """Set attachment metadata.

        :params volume_id: Id of the volume to update.
        :param instance_uuid: uuid of the attaching instance.
        """
        return self.driver.attach(volume_id, instance_uuid)

    def detach(self, volume_id, attachment_uuid):
        """Clear attachment metadata.

        :params volume_id: Id of the volume to update.
        :param attachment_uuid: The uuid of the volume attachment.
        """
        return self.driver.detach(volume_id, attachment_uuid)

""" this is contain Abstract Class and Quota Class
    for all block storage driver which we want to implement.
"""

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseDriver(object):

    def __init__(self, *args, **kwargs):
        super(BaseDriver, self).__init__()
        self.block_storage_quota = BaseQuota()

    @abc.abstractmethod
    def create(self, size, volume_type, **kwargs):
        """Create a volume

        :param size: Size of volume in GB
        :param volume_type: Type of volume.
        :param **kwargs: Arbitrary keyword arguments.
        """
        return

    @abc.abstractmethod
    def get(self, volume_id):
        """Get a volume.

        :param volume_id: The ID of the volume to get.
        """
        return

    @abc.abstractmethod
    def list(self, **kwargs):
        """List all volumes.

        :param **kwargs: Arbitrary keyword arguments.
        """
        return

    @abc.abstractmethod
    def delete(self, volume_id):
        """Delete a volume.

        :param volume_id: Id of the volume to delete.
        """
        return

    @abc.abstractmethod
    def update(self, volume_id, **kwargs):
        """Update the name or description for a volume.

        :params volume_id: Id of the volume to update.
        :param **kwargs: Arbitrary keyword arguments.
        """
        return

    @abc.abstractmethod
    def attach(self, volume_id, instance_uuid):
        """Set attachment metadata.

        :params volume_id: Id of the volume to update.
        :param instance_uuid: uuid of the attaching instance.
        """
        return

    @abc.abstractmethod
    def detach(self, volume_id, attachment_uuid):
        """Clear attachment metadata.

        :params volume_id: Id of the volume to update.
        :param attachment_uuid: The uuid of the volume attachment.
        """
        return


class BaseQuota(object):
    """ Class about Block Storage Quota"""
    def __init__(self):
        self._setup()

    def _setup(*args, **kwargs):
        pass

    def get(self):
        """ Get quota from Cloud Provider """

        # get all block storage from Cloud provider
        attrs = ("volumes",
                 "snapshots",
                 "gigabytes")
        for attr in attrs:
            setattr(self, attr, eval("self.get_{}()" . format(attr)))

    def set(self, attr, value):
        """ Update quota for block storage """
        # set specific attribute
        setattr(self, attr, value)

    def get_volumes(self):
        """ Return volumes - Number of Block Storage volumes allowed
        per tenant/project """
        pass

    def get_snapshots(self):
        """ Return snapshots - Number of Block Storage snapshots allowed
        per tenant/project. """
        pass

    def get_volume_gigabytes(self):
        """ Return gigabytes - Number of volume gigabytes allowed
        per tenant. """
        pass

    def get_backup_gigabytes(self):
        """ Return gigabytes - Number of backup gigabytes allowed
        per tenant. """
        pass

    def get_backups(self):
        """ Return backups """
        pass

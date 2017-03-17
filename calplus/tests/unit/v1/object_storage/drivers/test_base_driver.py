from calplus.tests import base
from calplus.v1.object_storage.drivers.base import BaseDriver


class RightFakeDriver(BaseDriver):
    """FakeDriver implemented all of BaseDriver methods.
    """

    def __init__(self):
        super(RightFakeDriver, self).__init__()

    def create_container(self, container, **kwargs):
        return 'fake_result'

    def delete_container(self, container):
        return 'fake_result'

    def list_containers(self):
        return 'fake_result'

    def stat_container(self, container):
        return 'fake_result'

    def update_container(self, container, headers, **kwargs):
        return 'fake_result'

    def upload_object(self, container, obj, content,
                      content_length=None, **kwargs):
        return 'fake_result'

    def download_object(self, container, obj, **kwargs):
        return 'fake_result'

    def stat_object(self, container, obj):
        return 'fake_result'

    def delete_object(self, container, obj, **kwargs):
        return 'fake_result'

    def list_container_objects(self, container, prefix=None, delimiter=None):
        return 'fake_result'

    def update_object(self, container, obj, headers, **kwargs):
        return 'fake_result'

    def copy_object(self, container, obj, destination=None, **kwargs):
        return 'fake_result'


class WrongFakeDriver(BaseDriver):

    def __init__(self):
        super(WrongFakeDriver, self).__init__()


class ObjectStorageBaseDriverTest(base.TestCase):

    """Testing class for ObjectStorage BaseDriver"""

    def setUp(self):
        super(ObjectStorageBaseDriverTest, self).setUp()

    def test_init_instance_of_childbasedriver(self):
        fake_driver = RightFakeDriver()
        self.assertIsInstance(fake_driver, RightFakeDriver)

    def test_unable_to_init_instance_of_childbasedriver(self):
        self.assertRaises(TypeError, WrongFakeDriver)

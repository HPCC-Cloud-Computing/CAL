""" OpenstackDriver for Network
    based on NetworkDriver
"""


from cal.tests import base
from cal.v1.network.drivers.network_driver import NetworkDriver


class NetWorkDriverTest(base.TestCase):

    """Testing class for NetWorkDriver"""

    def setUp(self):
        super(NetWorkDriverTest, self).setUp()
        self.fake_driver = NetworkDriver()

    def test_create(self):
        self.assertRaises(NotImplementedError,
            self.fake_driver.create)

    def test_show(self):
        self.assertRaises(NotImplementedError,
            self.fake_driver.show)

    def test_list(self):
        self.assertRaises(NotImplementedError,
            self.fake_driver.list)

    def test_update(self):
        self.assertRaises(NotImplementedError,
            self.fake_driver.update)

    def test_delete(self):
        self.assertRaises(NotImplementedError,
            self.fake_driver.delete)

    def test_set_quota(self):
        self.fake_driver.network_quota.set('fake_attribute', 'fake_value')

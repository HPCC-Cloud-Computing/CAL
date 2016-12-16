from calplus.tests import base
from calplus.v1 import utils
from calplus import exceptions


class TestUtils(base.TestCase):
    """docstring for TestUtils"""

    def setUp(self):
        super(TestUtils, self).setUp()

    def test_validate_driver_successfully(self):

        def test_connection():
            return True

        @utils.validate_driver(test_connection)
        def fake_validate_driver(driver=None):
            if driver:
                return True
            else:
                return False

        self.assertEqual(True, fake_validate_driver('default'))
        self.assertEqual(False, fake_validate_driver())

    def test_validate_driver_error(self):

        def test_connection_false():
            return False

        @utils.validate_driver(test_connection_false)
        def fake_validate_driver_false(driver=None):
            return True

        self.assertRaises(exceptions.ProviderNotValidate,
                          fake_validate_driver_false, 'default')
        self.assertRaises(exceptions.ProviderNotValidate,
                         fake_validate_driver_false)

from calplus.tests import base
from calplus.v1 import utils


class TestUtils(base.TestCase):

    """docstring for TestUtils"""

    def setUp(self):
        super(TestUtils, self).setUp()

    def test_get_all_driver(self):
        drivers = utils.get_all_driver()
        self.assertEqual([], drivers)

    def test_validate_driver(self):
        @utils.validate_driver
        def test(request, drivers):
            pass

        import inspect
        args = inspect.getargspec(test).args
        self.assertEqual(['request'], args)

from calplus.tests import base
from calplus.utils import set_config_file, get_list_providers
import calplus.conf


class ClientTest(base.TestCase):

    """docstring for ClientTest"""

    def setUp(self):
        super(ClientTest, self).setUp()
        self.fake_conf = calplus.conf.CONF

    def test_set_config_file_not_found(self):
        set_config_file('calplus/tests/fake_config_file.conf')

        self.assertEqual(
            ['calplus/tests/fake_config_file.conf'],
            self.fake_conf.config_file
        )

    def test_get_list_providers(self):
        set_config_file('calplus/tests/fake_config_file.conf')
        list_providers = get_list_providers()

        self.assertEqual(3, len(list_providers))

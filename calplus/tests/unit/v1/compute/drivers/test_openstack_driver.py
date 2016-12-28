""" OpenstackDriver for Compute
    based on BaseDriver for Compute Resource
"""


import mock

from keystoneauth1.exceptions.base import ClientException

from calplus.tests import base
from calplus.v1.compute.drivers.openstack import OpenstackDriver

fake_config_driver = {
    'os_auth_url': 'http://controller:5000/v2_0',
    'os_username': 'test',
    'os_password': 'veryhard',
    'os_project_name': 'demo',
    'os_endpoint_url': 'http://controller:9696',
    'os_driver_name': 'default',
    'os_project_domain_name': 'default',
    'os_user_domain_name': 'default',
    'tenant_id': 'fake_tenant_id',
    'limit': {
        "subnet": 10,
        "network": 10,
        "floatingip": 50,
        "subnetpool": -1,
        "security_group_rule": 100,
        "security_group": 10,
        "router": 10,
        "rbac_policy": -1,
        "port": 50
    }
}


class FakeFloatingIPNotAssociate(object):

    def to_dict(self):
        dict = {
            'instance_id': None,
            'ip': 'fake_public_ip',
            'fixed_ip': None,
            'id': 'fake_public_ip_id',
            'pool': 'provider-net'
        }
        return dict


class FakeFloatingIP(object):

    def to_dict(self):
        dict = {
            'instance_id': 'fake_instance_id',
            'ip': 'fake_public_ip',
            'fixed_ip': 'fake_privte_ip',
            'id': 'fake_public_ip_id',
            'pool': 'provider-net'
        }
        return dict


class FakeFlavor(object):

    def __init__(self, id):
        super(FakeFlavor, self).__init__()
        self.id = id


class FakeServer(object):
    """in fact: mock.Mock is novaclient.v2.servers.Server
    """
    def __init__(self):
        super(FakeServer, self).__init__()
        self.id = 'fake_id'

    def to_dict(self):
        return {
            'id': self.id
        }


class OpenstackDriverTest(base.TestCase):

    """docstring for OpenstackDriverTest"""

    def setUp(self):
        super(OpenstackDriverTest, self).setUp()
        self.fake_driver = OpenstackDriver(fake_config_driver)

    def test_create_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'create',
            mock.Mock(return_value=FakeServer()))

        self.fake_driver.create(
            'fake_image_id',
            'fake_flavor_id',
            'fake_net_id',
            'fake_name'
        )

        self.fake_driver.client.servers.create.\
            assert_called_once_with(
                name='fake_name',
                image='fake_image_id',
                flavor='fake_flavor_id',
                nics=[{'net-id': 'fake_net_id'}]
            )

    def test_create_without_instance_name(self):
        self.mock_object(
            self.fake_driver.client.servers, 'create',
            mock.Mock(return_value=FakeServer()))

        self.fake_driver.create(
            'fake_image_id',
            'fake_flavor_id',
            'fake_net_id'
        )

        self.fake_driver.client.servers.create. \
            assert_called_once_with(
                name=mock.ANY,
                image='fake_image_id',
                flavor='fake_flavor_id',
                nics=[{'net-id': 'fake_net_id'}]
            )

    def test_create_unable_to_create_instance(self):
        self.mock_object(
            self.fake_driver.client.servers, 'create',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.create,
                'fake_image_id',
                'fake_flavor_id',
                'fake_net_id',
                'fake_name')

        self.fake_driver.client.servers.create. \
            assert_called_once_with(
                name='fake_name',
                image='fake_image_id',
                flavor='fake_flavor_id',
                nics=[{'net-id': 'fake_net_id'}]
            )

    def test_show_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'get',
            mock.Mock(return_value=mock.Mock))
        # NOTE: in fact: mock.Mock is novaclient.v2.servers.Server

        self.fake_driver.show('fake_id')

        self.fake_driver.client.servers.get. \
            assert_called_once_with('fake_id')

    def test_show_unable_to_show(self):
        self.mock_object(
            self.fake_driver.client.servers, 'get',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.show, 'fake_id')

        self.fake_driver.client.servers.get. \
            assert_called_once_with('fake_id')

    def test_list_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'list',
            mock.Mock(return_value=[mock.Mock, mock.Mock]))
        # NOTE: in fact: return_value is novaclient.base.ListWithMeta
        # And return_value[0] is novaclient.v2.servers.Server

        self.fake_driver.list()

        self.fake_driver.client.servers.list. \
            assert_called_once_with()

    def test_list_unable_to_list(self):
        self.mock_object(
            self.fake_driver.client.servers, 'list',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.list)

        self.fake_driver.client.servers.list. \
            assert_called_once_with()

    def test_delete_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'delete',
            mock.Mock(return_value=True))

        self.fake_driver.delete('fake_id')

        self.fake_driver.client.servers.delete. \
            assert_called_once_with('fake_id')

    def test_delete_unable_to_delete(self):
        self.mock_object(
            self.fake_driver.client.servers, 'delete',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.delete, 'fake_id')

        self.fake_driver.client.servers.delete. \
            assert_called_once_with('fake_id')

    def test_shutdown_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'stop',
            mock.Mock(return_value=True))

        self.fake_driver.shutdown('fake_id')

        self.fake_driver.client.servers.stop. \
            assert_called_once_with('fake_id')

    def test_shutdown_unable_to_shutdown(self):
        self.mock_object(
            self.fake_driver.client.servers, 'stop',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.shutdown, 'fake_id')

        self.fake_driver.client.servers.stop. \
            assert_called_once_with('fake_id')

    def test_start_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'start',
            mock.Mock(return_value=True))

        self.fake_driver.start('fake_id')

        self.fake_driver.client.servers.start. \
            assert_called_once_with('fake_id')

    def test_start_unable_to_start(self):
        self.mock_object(
            self.fake_driver.client.servers, 'start',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.start, 'fake_id')

        self.fake_driver.client.servers.start. \
            assert_called_once_with('fake_id')

    def test_reboot_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'reboot',
            mock.Mock(return_value=True))

        self.fake_driver.reboot('fake_id')

        self.fake_driver.client.servers.reboot. \
            assert_called_once_with('fake_id')

    def test_reboot_unable_to_reboot(self):
        self.mock_object(
            self.fake_driver.client.servers, 'reboot',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.reboot, 'fake_id')

        self.fake_driver.client.servers.reboot. \
            assert_called_once_with('fake_id')

    def test_resize_successfully(self):
        self.mock_object(
            self.fake_driver.client.flavors, 'find',
            mock.Mock(return_value=FakeFlavor('fake_flavor_id')))
        # in fact: return_value is novaclient.v2.flavors.Flavor
        self.mock_object(
            self.fake_driver.client.servers, 'resize',
            mock.Mock(return_value=()))
        # in fact: return_value is novaclient.base.TupleWithMeta
        # printable : ()
        self.mock_object(
            self.fake_driver.client.servers, 'confirm_resize',
            mock.Mock(return_value=()))
        # in fact: return_value is novaclient.base.TupleWithMeta
        # printable : ()
        self.mock_object(
            self.fake_driver.client.servers, 'revert_resize',
            mock.Mock())

        self.assertEqual(True,
            self.fake_driver.resize('fake_id', 'fake_flavor_name'))

        self.fake_driver.client.flavors.find. \
            assert_called_once_with(name='fake_flavor_name')
        self.fake_driver.client.servers.resize. \
            assert_called_once_with('fake_id', 'fake_flavor_id')
        self.fake_driver.client.servers.confirm_resize. \
            assert_called_once_with('fake_id')
        self.assertFalse(
            self.fake_driver.client.servers.revert_resize.called)

    def test_resize_can_not_find_flavor(self):
        self.mock_object(
            self.fake_driver.client.flavors, 'find',
            mock.Mock(side_effect=ClientException))
        # Detail: NotFound will be raise
        self.mock_object(
            self.fake_driver.client.servers, 'resize',
            mock.Mock())
        self.mock_object(
            self.fake_driver.client.servers, 'confirm_resize',
            mock.Mock())
        self.mock_object(
            self.fake_driver.client.servers, 'revert_resize',
            mock.Mock())

        self.assertRaises(ClientException,
            self.fake_driver.resize, 'fake_id', 'fake_flavor_name')

        self.fake_driver.client.flavors.find. \
            assert_called_once_with(name='fake_flavor_name')
        self.assertFalse(
            self.fake_driver.client.servers.resize.called)
        self.assertFalse(
            self.fake_driver.client.servers.confirm_resize.called)
        self.assertFalse(
            self.fake_driver.client.servers.revert_resize.called)

    def test_resize_can_not_confirm_resize(self):
        self.mock_object(
            self.fake_driver.client.flavors, 'find',
            mock.Mock(return_value=FakeFlavor('fake_flavor_id')))
        # in fact: return_value is novaclient.v2.flavors.Flavor
        self.mock_object(
            self.fake_driver.client.servers, 'resize',
            mock.Mock(return_value=()))
        # in fact: return_value is novaclient.base.TupleWithMeta
        # printable : ()
        self.mock_object(
            self.fake_driver.client.servers, 'confirm_resize',
            mock.Mock(side_effect=ClientException))
        # in fact: return_value is novaclient.base.TupleWithMeta
        # printable : ()
        self.mock_object(
            self.fake_driver.client.servers, 'revert_resize',
            mock.Mock(return_value=()))

        self.assertEqual(False,
            self.fake_driver.resize('fake_id', 'fake_flavor_name'))

        self.fake_driver.client.flavors.find. \
            assert_called_once_with(name='fake_flavor_name')
        self.fake_driver.client.servers.resize. \
            assert_called_once_with('fake_id', 'fake_flavor_id')
        self.fake_driver.client.servers.confirm_resize. \
            assert_called_once_with('fake_id')
        self.fake_driver.client.servers.revert_resize. \
            assert_called_once_with('fake_id')

    def test_resize_can_not_resize(self):
        self.mock_object(
            self.fake_driver.client.flavors, 'find',
            mock.Mock(return_value=FakeFlavor('fake_flavor_id')))
        # in fact: return_value is novaclient.v2.flavors.Flavor
        self.mock_object(
            self.fake_driver.client.servers, 'resize',
            mock.Mock(side_effect=ClientException))
        # in fact: return_value is novaclient.base.TupleWithMeta
        # printable : ()
        self.mock_object(
            self.fake_driver.client.servers, 'confirm_resize',
            mock.Mock())
        self.mock_object(
            self.fake_driver.client.servers, 'revert_resize',
            mock.Mock())

        self.assertRaises(ClientException,
            self.fake_driver.resize, 'fake_id', 'fake_flavor_name')

        self.fake_driver.client.flavors.find. \
            assert_called_once_with(name='fake_flavor_name')
        self.fake_driver.client.servers.resize. \
            assert_called_once_with('fake_id', 'fake_flavor_id')
        self.assertFalse(
            self.fake_driver.client.servers.confirm_resize.called)
        self.assertFalse(
            self.fake_driver.client.servers.revert_resize.called)

    def test_resize_can_not_revert(self):
        self.mock_object(
            self.fake_driver.client.flavors, 'find',
            mock.Mock(return_value=FakeFlavor('fake_flavor_id')))
        # in fact: return_value is novaclient.v2.flavors.Flavor
        self.mock_object(
            self.fake_driver.client.servers, 'resize',
            mock.Mock(return_value=()))
        # in fact: return_value is novaclient.base.TupleWithMeta
        # printable : ()
        self.mock_object(
            self.fake_driver.client.servers, 'confirm_resize',
            mock.Mock(side_effect=ClientException))
        # in fact: return_value is novaclient.base.TupleWithMeta
        # printable : ()
        self.mock_object(
            self.fake_driver.client.servers, 'revert_resize',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.resize, 'fake_id', 'fake_flavor_name')

        self.fake_driver.client.flavors.find. \
            assert_called_once_with(name='fake_flavor_name')
        self.fake_driver.client.servers.resize. \
            assert_called_once_with('fake_id', 'fake_flavor_id')
        self.fake_driver.client.servers.confirm_resize. \
            assert_called_once_with('fake_id')
        self.fake_driver.client.servers.revert_resize. \
            assert_called_once_with('fake_id')

    def test_add_nic_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'interface_attach',
            mock.Mock(return_value=mock.Mock))
        # NOTE: in fact: mock.Mock is novaclient.v2.servers.Server
        # but It have port_id and net_id attribute, != nornal Server object

        self.fake_driver.add_nic('fake_id', 'fake_net_id')

        self.fake_driver.client.servers.interface_attach. \
            assert_called_once_with('fake_id', None, 'fake_net_id', None)

    def test_add_nic_unable_to_add(self):
        self.mock_object(
            self.fake_driver.client.servers, 'interface_attach',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.add_nic, 'fake_id', 'fake_net_id')

        self.fake_driver.client.servers.interface_attach. \
            assert_called_once_with('fake_id', None, 'fake_net_id', None)

    def test_delete_nic_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'interface_detach',
            mock.Mock(return_value=mock.Mock))
        # NOTE: in fact: mock.Mock is novaclient.base.TupleWithMeta
        # printable: ()

        self.fake_driver.delete_nic('fake_id', 'fake_port_id')

        self.fake_driver.client.servers.interface_detach. \
            assert_called_once_with('fake_id', 'fake_port_id')

    def test_delete_nic_unable_to_delete(self):
        self.mock_object(
            self.fake_driver.client.servers, 'interface_detach',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.delete_nic, 'fake_id', 'fake_port_id')

        self.fake_driver.client.servers.interface_detach. \
            assert_called_once_with('fake_id', 'fake_port_id')

    def test_list_nic_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'interface_list',
            mock.Mock(return_value=[mock.Mock, mock.Mock]))
        # NOTE: in fact: return_value is novaclient.base.ListWithMeta
        # And return_value[0] is novaclient.v2.servers.Server
        # just call to_dict() for each item to use them easier

        self.fake_driver.list_nic('fake_id')

        self.fake_driver.client.servers.interface_list. \
            assert_called_once_with('fake_id')

    def test_list_nic_unable_to_list(self):
        self.mock_object(
            self.fake_driver.client.servers, 'interface_list',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.list_nic, 'fake_id')

        self.fake_driver.client.servers.interface_list. \
            assert_called_once_with('fake_id')

    def test_associate_public_ip_successfully(self):
        self.mock_object(
            self.fake_driver.client.floating_ips, 'get',
            mock.Mock(return_value=FakeFloatingIPNotAssociate()))
        # NOTE: return_value is novaclient.v2.floating_ips.FloatingIP
        self.mock_object(
            self.fake_driver.client.servers, 'add_floating_ip',
            mock.Mock(return_value=()))

        self.fake_driver.associate_public_ip(
            'fake_id', 'fake_public_ip_id')

        self.fake_driver.client.floating_ips.get. \
            assert_called_once_with('fake_public_ip_id')
        self.fake_driver.client.servers.add_floating_ip. \
            assert_called_once_with(
                'fake_id', 'fake_public_ip', None
            )

    def test_associate_public_ip_unable_to_get_floating_ip(self):
        self.mock_object(
            self.fake_driver.client.floating_ips, 'get',
            mock.Mock(side_effect=ClientException))
        self.mock_object(
            self.fake_driver.client.servers, 'add_floating_ip',
            mock.Mock())

        self.assertRaises(ClientException,
            self.fake_driver.associate_public_ip,
                          'fake_id', 'fake_public_ip_id')

        self.fake_driver.client.floating_ips.get. \
            assert_called_once_with('fake_public_ip_id')
        self.assertFalse(
            self.fake_driver.client.servers.add_floating_ip.called)

    def test_associate_public_ip_unable_to_add_floating_ip(self):
        self.mock_object(
            self.fake_driver.client.floating_ips, 'get',
            mock.Mock(return_value=FakeFloatingIPNotAssociate()))
        # NOTE: return_value is novaclient.v2.floating_ips.FloatingIP
        self.mock_object(
            self.fake_driver.client.servers, 'add_floating_ip',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.associate_public_ip,
                          'fake_id', 'fake_public_ip_id')

        self.fake_driver.client.floating_ips.get. \
            assert_called_once_with('fake_public_ip_id')
        self.fake_driver.client.servers.add_floating_ip. \
            assert_called_once_with(
                'fake_id', 'fake_public_ip', None
            )

    def test_disassociate_public_ip_successfully(self):
        self.mock_object(
            self.fake_driver.client.floating_ips, 'get',
            mock.Mock(return_value=FakeFloatingIP()))
        # NOTE: return_value is novaclient.v2.floating_ips.FloatingIP
        self.mock_object(
            self.fake_driver.client.servers, 'remove_floating_ip',
            mock.Mock(return_value=()))

        self.fake_driver.disassociate_public_ip('fake_public_ip_id')

        self.fake_driver.client.floating_ips.get. \
            assert_called_once_with('fake_public_ip_id')
        self.fake_driver.client.servers.remove_floating_ip. \
            assert_called_once_with(
                'fake_instance_id', 'fake_public_ip'
            )

    def test_disassociate_public_ip_unable_to_get_floating_ip(self):
        self.mock_object(
            self.fake_driver.client.floating_ips, 'get',
            mock.Mock(side_effect=ClientException))
        self.mock_object(
            self.fake_driver.client.servers, 'remove_floating_ip',
            mock.Mock())

        self.assertRaises(ClientException,
            self.fake_driver.disassociate_public_ip, 'fake_public_ip_id')

        self.fake_driver.client.floating_ips.get. \
            assert_called_once_with('fake_public_ip_id')
        self.assertFalse(
            self.fake_driver.client.servers.remove_floating_ip.called)

    def test_disassociate_public_ip_unable_to_remove_floating_ip(self):
        self.mock_object(
            self.fake_driver.client.floating_ips, 'get',
            mock.Mock(return_value=FakeFloatingIP()))
        # NOTE: return_value is novaclient.v2.floating_ips.FloatingIP
        self.mock_object(
            self.fake_driver.client.servers, 'remove_floating_ip',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.disassociate_public_ip, 'fake_public_ip_id')

        self.fake_driver.client.floating_ips.get. \
            assert_called_once_with('fake_public_ip_id')
        self.fake_driver.client.servers.remove_floating_ip. \
            assert_called_once_with(
                'fake_instance_id', 'fake_public_ip'
            )

    def test_list_ip_successfully(self):
        self.mock_object(
            self.fake_driver.client.servers, 'ips',
            mock.Mock(return_value={'Int-net': 'fake_list'}))
        # NOTE: in fact: mock.Mock is novaclient.base.DictWithMeta
        # printable: show a dict

        self.fake_driver.list_ip('fake_id')

        self.fake_driver.client.servers.ips. \
            assert_called_once_with('fake_id')

    def test_list_ip_unable_to_delete(self):
        self.mock_object(
            self.fake_driver.client.servers, 'ips',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_driver.list_ip, 'fake_id')

        self.fake_driver.client.servers.ips. \
            assert_called_once_with('fake_id')

"""Provider Configuration"""
from oslo_config import cfg


# Openstack Authenticate Configuration.
openstack_group = cfg.OptGroup('openstack1',
                         title='OpenStack Hosts')

openstack_opts = [
    cfg.StrOpt('driver_name',
               default='OpenStackHUST'),
    cfg.StrOpt('type_driver',
               default='openstack'),
    cfg.StrOpt('os_auth_url',
               default='localhost'),
    cfg.StrOpt('os_project_name',
               default='admin'),
    cfg.StrOpt('os_username',
               default='admin'),
    cfg.StrOpt('os_password',
               default='ADMIN_PASS'),
    cfg.StrOpt('os_project_domain_name',
               default='default'),
    cfg.StrOpt('os_user_domain_name',
               default='default'),
    cfg.IntOpt('os_identity_api_version',
               default='3'),
    cfg.IntOpt('os_image_api_version',
               default='2'),
    cfg.StrOpt('tenant_id',
               default=''),
    cfg.StrOpt('os_novaclient_version',
               default='2.1'),
    cfg.DictOpt('limit',
                default={
                     "subnet": 10,
                     "network": 10,
                     "floatingip": 50,
                     "subnetpool": -1,
                     "security_group_rule": 100,
                     "security_group": 10,
                     "router": 10,
                     "rbac_policy": -1,
                     "port": 50
                })
]

# Amazon Authenticate Configuration.
amazon_group = cfg.OptGroup('amazon1',
                      title='Amazon Hosts')

amazon_opts = [
    cfg.StrOpt('driver_name',
               default='AmazonHUSTACC'),
    cfg.StrOpt('type_driver',
               default='amazon'),
    cfg.StrOpt('aws_access_key_id',
               default='localhost'),
    cfg.StrOpt('aws_secret_access_key',
               default='admin'),
    cfg.StrOpt('region_name',
               default='localhost'),
    cfg.StrOpt('endpoint_url',
               default='http://localhost:35357/v3/'),
    cfg.DictOpt('limit',
                default={
                    "subnet": 10,
                    "vpc": 5,
                    "floatingip": 50,
                    "subnetpool": -1,
                    "security_group_rule": 100,
                    "security_group": 10,
                    "router": 10,
                    "rbac_policy": -1,
                    "port": 50
                })
]

#Provider Configuration
provider_group = cfg.OptGroup('providers',
                              title='Supported Providers')

enable_drivers = cfg.ListOpt(
    'enable_drivers',
    default=[
        openstack_group.name,
        amazon_group.name
    ],
    help='List of available Driver Hosts'
)

driver_mapper = cfg.DictOpt('driver_mapper',
                            default={
                                'openstack': 'OpenstackDriver',
                                'amazon': 'AmazonDriver',
                            },
                            help="""
                            Dict with key is provider, and value is
                            Driver class.
                            """)

provider_opts = [
    driver_mapper,
    enable_drivers
]


def register_opts(conf):
    conf.register_group(provider_group)
    conf.register_opts(provider_opts, group=provider_group)

    conf.register_group(openstack_group)
    conf.register_opts(openstack_opts, group=openstack_group)

    conf.register_group(amazon_group)
    conf.register_opts(amazon_opts, group=amazon_group)


def list_opts():
    return {
        provider_group: provider_opts,
        openstack_group: openstack_opts,
        amazon_group: amazon_opts,
    }

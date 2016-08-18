"""Provider Configuration"""
from oslo_config import cfg


provider_group = cfg.OptGroup('providers',
                              title='Supported Providers')

supported_providers = cfg.ListOpt('supported_providers',
                    default=['openstack', 'amazon', 'opennebula'],
                    help='List of supported provider enabled by default')

ALL_OPTS = [
    supported_providers,
]


def register_opts(conf):
    conf.register_group(provider_group)
    conf.register_opts(ALL_OPTS, group=provider_group)


def list_opts():
    return {provider_group: ALL_OPTS}

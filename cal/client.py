import logging

from cal import exceptions
from cal import conf
from cal.v1.compute import client as compute_client_v1
from cal.v1.network import client as network_client_v1
from cal.v1.block_storage import client as block_storage_client_v1
from cal.v1.object_storage import client as object_storage_client_v1
from cal.version import __version__

LOG = logging.getLogger(__name__)

CONF = conf.CONF

_CLIENTS = {
    '1.0.0': {
        'compute': compute_client_v1.Client,
        'network': network_client_v1.Client,
        'block_storage': block_storage_client_v1.Client,
        'object_storge': object_storage_client_v1.Client,
    }
}


def Client(version=__version__, resource=None,
           provider=None, **kwargs):
    """Initialize client object based on given version.

    :params version: version of CAL, define at setup.cfg
    :params resource: resource type
                     (network, compute, object_storage, block_storage)
    :params provider: cloud provider(Openstack, Amazon...)
    :params **kwargs: specific args for resource
    :return: class Client

    HOW-TO:
    The simplest way to create a client instance is initialization::

        >> from cal import client
        >> cal = client.Client(version='1.0.0',
                               resource='compute',
                               provider='OpenStack',
                               some_needed_args_for_ComputeClient)
    """

    versions = _CLIENTS.keys()
    providers = CONF.providers.supported_providers
    resources = _CLIENTS[version].keys()

    if version not in versions:
        raise exceptions.UnsupportedVersion(
            'Unknown client version or subject'
        )

    if provider.lower() not in providers:
        raise exceptions.ProviderNotFound(
            'Unknow provider'
        )

    if resource.lower() not in resources:
        raise exceptions.ResourceNotFound(
            'Unknow resource: compute, network,\
                        object_storage, block_storage'
        )

    LOG.info('Instantiating {} client ({})' . format(resource, version))

    return _CLIENTS[version][resource](provider, **kwargs)

from cal import errors
from cal.v1.compute import client as compute_client_v1
from cal.v1.network import client as network_client_v1
from cal.v1.storage import client as storage_client_v1
from cal.version import __version__

_CLIENTS = {
    '1.0.0': {
        'compute': compute_client_v1.Client,
        'network': network_client_v1.Client,
        'storge': storage_client_v1.Client,
    }
}


def Client(url=None, version=__version__,
           subject=None, provider=None, **kwargs):
    """Initialize client object based on given version.
    """
    try:
        return _CLIENTS[version][subject](url, provider, **kwargs)
    except KeyError:
        raise errors.CALError('Unknown client version or subject')

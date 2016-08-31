import logging
import importlib

import cal.conf

LOG = logging.getLogger(__name__)
CONF = cal.conf.CONF


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args,
                                                                  **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass


class BaseClient(Singleton):
    """Base Client
    :params path: module path of driver, for e.x: 'cal.v1.network.driver'
    :params provider: provider for e.x: 'OpenStack'
    :params cloud_config:
    """
    def __init__(self, path, provider, cloud_config):
        self.driver = None
        self.set_driver(path, provider, cloud_config)

    def set_driver(self, path, provider, cloud_config):
        _provider = provider.lower()
        module = importlib.import_module(path + '.' + _provider)
        LOG.info('Use %s driver for client', _provider)
        _driver = CONF.providers.driver_mapper[_provider]
        self.driver = getattr(module, _driver)(cloud_config)

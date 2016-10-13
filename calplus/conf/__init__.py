from oslo_config import cfg

from calplus.conf import block_storage
from calplus.conf import compute
from calplus.conf import network
from calplus.conf import object_storage
from calplus.conf import providers
from calplus.conf import wsgi

CONF = cfg.CONF

block_storage.register_opts(CONF)
compute.register_opts(CONF)
network.register_opts(CONF)
object_storage.register_opts(CONF)
providers.register_opts(CONF)
wsgi.register_opts(CONF)

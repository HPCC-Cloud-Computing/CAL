from oslo_config import cfg

from cal.conf import block_storage
from cal.conf import compute
from cal.conf import network
from cal.conf import object_storage
from cal.conf import providers
from cal.conf import wsgi

CONF = cfg.CONF

block_storage.register_opts(CONF)
compute.register_opts(CONF)
network.register_opts(CONF)
object_storage.register_opts(CONF)
providers.register_opts(CONF)
wsgi.register_opts(CONF)

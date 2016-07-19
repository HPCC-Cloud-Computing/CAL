from oslo_config import cfg

from cal.conf import network
from cal.conf import wsgi

CONF = cfg.CONF

network.register_opts(CONF)
wsgi.register_opts(CONF)

from oslo_config import cfg
from cal.conf import wsgi

CONF = cfg.CONF

wsgi.register_opts(CONF)

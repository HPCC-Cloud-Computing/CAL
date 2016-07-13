# from paste import httpserver
from oslo_config import cfg
from paste.deploy import loadapp
from werkzeug import serving
import socket

from oslo_config import cfg
# from oslo_utils import netutils

CONF = cfg.CONF


service_opts = [
    # cfg.StrOpt('my_ip',
    #            default=netutils.get_my_ipv4(),
    #            help='IP address of this host'),
    # cfg.StrOpt('my_block_storage_ip',
    #            default='$my_ip',
    #            help='Block storage IP address of this host'),
    # cfg.StrOpt('host',
    #            default=socket.gethostname(),
    #            help='Name of this node.  This can be an opaque identifier.  '
    #                 'It is not necessarily a hostname, FQDN, or IP address. '
    #                 'However, the node name must be valid within '
    #                 'an AMQP key, and if using ZeroMQ, a valid '
    #                 'hostname, FQDN, or IP address'),
    # cfg.BoolOpt('use_ipv6',
    #             default=False,
    #             help='Use IPv6'),
    cfg.StrOpt('cal_listen',
               default="0.0.0.0",
               help='The IP address on which the OpenStack API will listen.'),
    cfg.IntOpt('cal_listen_port',
               default=8080,
               min=1,
               max=65535,
               help='The port on which the OpenStack API will listen.'),
    cfg.StrOpt('cal_paste_file',
               default="/home/techbk/PycharmProjects/CAL/etc/cal/cal-paste.ini",
               help="The paste.deploy config file.")
]

CONF.register_opts(service_opts)

# INI_PATH = "config:{}".format(os.path.abspath("cal-paste.ini"))
INI_PATH = "config:{}".format(CONF.cal_paste_file)

wsgi_app = loadapp(INI_PATH, name='cal')

def main():
    host = getattr(CONF, 'cal_listen', '0.0.0.0')
    port = getattr(CONF, 'cal_listen_port', 8080)
    serving.run_simple(host, port, wsgi_app, use_debugger=True)
    # httpserver.serve(wsgi_app, host='0.0.0.0', port=8080)
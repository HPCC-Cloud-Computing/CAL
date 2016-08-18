"""WSGI Configuration"""
from oslo_config import cfg


wsgi_group = cfg.OptGroup('wsgi',
                          title='WSGI Options')

wsgi_log_format = cfg.StrOpt(
    'wsgi_log_format',
    default='%(client_ip)s "%(request_line)s" status: %(status_code)s'
            ' len: %(body_length)s time: %(wall_seconds).7f',
    deprecated_group='DEFAULT',
    help="""
It represents a python format string that is used as the template to generate
log lines. The following values can be formatted into it: client_ip,
date_time, request_line, status_code, body_length, wall_seconds.
This option is used for building custom request loglines.
Possible values:
 * '%(client_ip)s "%(request_line)s" status: %(status_code)s'
   'len: %(body_length)s time: %(wall_seconds).7f' (default)
 * Any formatted string formed by specific values.
"""
)

wsgi_host = cfg.IPOpt(
    'host',
    default='0.0.0.0',
    help='Address on which the self-hosting server will listen'
)

wsgi_port = cfg.PortOpt(
    'port',
    default=8888,
    help='Port on which the self-hosting server will listen.'
)

ALL_OPTS = [
    wsgi_log_format,
    wsgi_host,
    wsgi_port,
]


def register_opts(conf):
    conf.register_group(wsgi_group)
    conf.register_opts(ALL_OPTS, group=wsgi_group)


def list_opts():
    return {wsgi_group: ALL_OPTS}

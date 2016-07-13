from oslo_config import cfg
from oslo_db import options
from oslo_log import log

from nova import debugger
from nova import paths
from nova import rpc
from nova import version


CONF = cfg.CONF

def parse_args(argv, default_config_files=None):
    # log.set_defaults(_DEFAULT_LOGGING_CONTEXT_FORMAT, _DEFAULT_LOG_LEVELS)
    log.register_options(CONF)
    options.set_defaults(CONF, connection=_DEFAULT_SQL_CONNECTION,
                         sqlite_db='nova.sqlite')
    rpc.set_defaults(control_exchange='nova')
    debugger.register_cli_opts()
    CONF(argv[1:],
         project='cal',
         version=version.version_string(),
         default_config_files=default_config_files)
    rpc.init(CONF)

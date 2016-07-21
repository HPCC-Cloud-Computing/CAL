from oslo_config import cfg


network_group = cfg.OptGroup('network',
                             title='Network Options')

re_check_cycle_time = cfg.IntOpt(
    're_check_cycle_time',
    help="Re check cycle time",
)

expired_time = cfg.IntOpt(
    'expired_time',
    help="Define expired time",
)

ALL_OPTS = [
    re_check_cycle_time,
    expired_time,
]

def register_opts(conf):
    conf.register_group(network_group)
    conf.register_opts(ALL_OPTS, group=network_group)

def list_opts():
    return {network_group: ALL_OPTS} 
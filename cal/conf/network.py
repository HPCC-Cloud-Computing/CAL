from oslo_config import cfg


network_group = cfg.OptGroup('network',
                             title='Network Options')

re_check_cycle_time = cfg.IntOpt(
    're_check_cycle_time',
    min=30,
    max=300,
    default=120,
    help="""
re_check_cycle_time(second) is option which is used by re-check thread
to re-check quota of each driver (may be re-check active state also).
For example:
"re_check_cycle_time=120" means re-check thread will re-update quota
of each driver per 120 secs.
""",
)

expired_time = cfg.IntOpt(
    'expired_time',
    min=200,
    max=600,
    default=300,
    help="""
Ex. "expired_time=300"(second) if the time from last_time_update (attribute
of quota object of driver), that driver quota was updated (by any ways:
re-check thread after process action ...) at, to now is longer than 300
secs, the driver quota will be updated.
""",
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

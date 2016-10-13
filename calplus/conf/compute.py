from oslo_config import cfg


compute_group = cfg.OptGroup('compute',
                             title='Compute Options')

# some config options here

driver_path = cfg.StrOpt(
    'driver_path',
    default='calplus.v1.compute.drivers',
    help='Default path to compute drivers',
)

ALL_OPTS = ([driver_path])


def register_opts(conf):
    conf.register_group(compute_group)
    conf.register_opts(ALL_OPTS, group=compute_group)


def list_opts():
    return {compute_group: ALL_OPTS}

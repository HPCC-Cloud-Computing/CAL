from oslo_config import cfg


block_storage_group = cfg.OptGroup('block_storage',
                                   title='Block Storage Options')

# some config options here

driver_path = cfg.StrOpt(
    'driver_path',
    default='cal.v1.block_storage.drivers',
    help='Default path to block storage drivers',
)

ALL_OPTS = ([driver_path])


def register_opts(conf):
    conf.register_group(block_storage_group)
    conf.register_opts(ALL_OPTS, group=block_storage_group)


def list_opts():
    return {block_storage_group: ALL_OPTS}

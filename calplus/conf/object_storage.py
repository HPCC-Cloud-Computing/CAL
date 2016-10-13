from oslo_config import cfg


object_storage_group = cfg.OptGroup('object_storage',
                                   title='Object Storage Options')

# some config options here

driver_path = cfg.StrOpt(
    'driver_path',
    default='calplus.v1.object_storage.drivers',
    help='Default path to object storage drivers',
)

ALL_OPTS = ([driver_path])


def register_opts(conf):
    conf.register_group(object_storage_group)
    conf.register_opts(ALL_OPTS, group=object_storage_group)


def list_opts():
    return {object_storage_group: ALL_OPTS}

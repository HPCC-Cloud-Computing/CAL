from oslo_config import cfg


network_group = cfg.OptGroup('network',
                             title='Network Options')

# some config options here 

ALL_OPTS = ()

def register_opts(conf):
    conf.register_group(network_group)
    conf.register_opts(ALL_OPTS, group=network_group)

def list_opts():
    return {network_group: ALL_OPTS} 
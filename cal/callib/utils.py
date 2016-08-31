import random

import cal.conf

CONF = cal.conf.CONF


def pick_cloud_provider():
    # Random pick one cloud provider.
    provider = list(CONF.providers.driver_mapper.keys())
    return random.choice(provider)


def pick_host_with_specific_provider(provider, cloud_config=None):
    if cloud_config is None:
        hosts = getattr(CONF, provider.lower())['hosts']
        # Now, random choice host from provider hosts.
        # TODO(kiennt): Next phase, pick the most optimized host
        #               of given provider.
        picked_host_config = hosts[random.choice(list(hosts.keys()))]
        return picked_host_config
    else:
        # TODO(kiennt): Check this cloud config: raise Exception
        #               if the given config is invalid (Must be a
        #               dict with the same keys like the one in
        #               conf/providers.py), or connection to this
        #               host is refused, broken...
        return cloud_config

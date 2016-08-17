""" this is contain Abstract Class and Quota Class
    for all network driver which we want to implement.
"""


class NetworkDriver(object):
    """abstract class for network driver"""

    def __init__(self):
        super(NetworkDriver, self).__init__()
        self.provider = "Unknown"
        self.network_quota = NetworkQuota()

    def create(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class NetworkQuota(object):
    """docstring for QuotaNetwork"""
    def __init__(self):
        super(NetworkQuota, self).__init__()
        self.get()

    def get(self):
        """Get quota from Cloud Provider."""

        # get all network quota from Cloud Provider.
        attrs = ("networks",
                "security_groups",
                "floating_ips",
                "routers",
                "internet_gateways",
                "vpn_gateways",
                "firewall")

        for attr in attrs:
            setattr(self, attr, eval("self.get_{}()". format(attr)))

    def set(self, attr, value):
        """Update quota for Network."""

        # set special attribute.
        setattr(self, attr, value)

    def get_networks(self):
        pass

    def get_security_groups(self):
        pass

    def get_floating_ips(self):
        pass

    def get_routers(self):
        pass

    def get_internet_gateways(self):
        pass

    def get_vpn_gateways(self):
        pass

    def get_firewall(self):
        pass

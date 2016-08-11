""" this is contain Abstract Class and Quota Class
    for all network driver which we want to implement.
"""


class NetworkDriver(object):

    """abstract class for network driver"""

    def __init__(self):
        super(NetworkDriver, self).__init__()
        self.provider = "Unknown"
        self.network_quota = NetworkQuota()

    def create():
        raise NotImplementedError

    def show():
        raise NotImplementedError

    def list():
        raise NotImplementedError

    def update():
        raise NotImplementedError

    def delete():
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
        return None

    def get_security_groups(self):
        return None

    def get_floating_ips(self):
        return None

    def get_routers(self):
        return None

    def get_internet_gateways(self):
        return None

    def get_vpn_gateways(self):
        return None

    def get_firewall(self):
        return None

""" OpenstackDriver for Network
    based on NetworkDriver
"""

from neutronclient.v2_0 import client
from network_driver import NetworkDriver, NetworkQuota


class OpenstackNetWorkDriver(NetworkDriver):

    """docstring for OpenstackNetWorkDriver"""

    def __init__(self, auth_url, project_name,
                 username, password, endpoint_url, **kargs):
        super(OpenstackNetWorkDriver, self).__init__()
        self.provider = "OPENSTACK"
        self.auth_url = auth_url
        self.project_name = project_name
        self.username = username
        self.password = password
        self.endpoint_url = endpoint_url
        self.driver_name = kargs.pop('driver_name', 'default')
        self._setup()

    def _setup(self):
        self.client = client.Client(
            username=self.username,
            password=self.password,
            project_name=self.project_name,
            auth_url=self.auth_url,
            endpoint_url=self.endpoint_url
        )
        self.network_quota = OpenstackNetworkQuota(self.client)

    def create(self, name, cidr, **kargs):
        admin_state_up = kargs.pop('admin_state_up', True)
        ip_version = kargs.pop('ip_version', 4)

        # step1: create network with empty name and admin_state_up
        network = {'name': '',
                   'admin_state_up': admin_state_up}
        net = self.client.create_network({'network': network}).get('network')
        network_id = net['id']

        # step 2: create subnet
        sub = {"network_id": network_id,
               "ip_version": ip_version,
               "cidr": cidr,
               "name": name}
        subnet = self.client.create_subnet({'subnet': sub}).get('subnet')

        result = {'name': subnet['name'],
                  'description': None,
                  'id': subnet['id'],
                  'cidr': subnet['cidr'],
                  'cloud': self.provider,
                  'gateway': subnet['gateway_ip'],
                  'security_group': None,
                  'allocation_pools': subnet['allocation_pools'],
                  'dns_nameservers': subnet['dns_nameservers']
                  }

        return result

    def show(self, subnet_id):
        subnet = self.client.show_subnet(subnet_id).get('subnet')

        result = {'name': subnet['name'],
                  'description': None,
                  'id': subnet['id'],
                  'cidr': subnet['cidr'],
                  'cloud': self.provider,
                  'gateway': subnet['gateway_ip'],
                  'security_group': None,
                  'allocation_pools': subnet['allocation_pools'],
                  'dns_nameservers': subnet['dns_nameservers']
                  }

        return result

    def list(self, **search_opts):
        subnets = self.client.list_subnets(**search_opts).get('subnets')
        result = []
        for subnet in subnets:
            sub = {'name': subnet['name'],
                   'description': None,
                   'id': subnet['id'],
                   'cidr': subnet['cidr'],
                   'cloud': self.provider,
                   'gateway': subnet['gateway_ip'],
                   'security_group': None,
                   'allocation_pools': subnet['allocation_pools'],
                   'dns_nameservers': subnet['dns_nameservers']
                   }
            result.append(sub)

        return result

    def update(self, network_id, network):
        # Now we can't update network, I'm trying again
        return None

    def delete(self, network_id):
        return self.client.delete_network(network_id)


class OpenstackNetworkQuota(NetworkQuota):
    """docstring for OpenstackNetworkQuota"""

    def __init__(self, client):
        super(NetworkQuota, self).__init__()
        self.client = client

    def get_networks(self):
        networks = {
                      "max": 50,
                      "used": 5,
                      "list_cidrs": [
                                  {"net_id": "net01", "cidr": "10.0.0.0/24"},
                                  {"net_id": "net01", "cidr": "10.0.1.0/24"},
                                  {"net_id": "net01", "cidr": "10.10.0.0/16"},
                                  {"net_id": "net01", "cidr": "10.20.0.0/16"},
                                  {"net_id": "net01", "cidr": "10.0.2.192/28"}
                              ],
                      "VPCs":
                      {
                          "max": 5,
                          "used": 1,
                          "list_cidrs": [
                              {
                                  "vpc_id": "vpc01",
                                  "cidr": "10.0.0.0/8"
                              }
                          ]
                      }
                    }

        return networks

    def get_security_groups(self):
        security_groups = {
                            "max": 50,
                            "used": 1,
                            "list_security_groups": [
                                {
                                    "security_group_id": "secgroup01",
                                    "rules_max": 50,
                                    "rules_used": 10,
                                    "list_rules": []
                                }
                            ]
                          }

        return security_groups

    def get_floating_ips(self):
        floating_ips = {
                          "max": 10,
                          "used": 5,
                          "list_floating_ips": []
                        }

        return floating_ips

    def get_routers(self):
        routers = {
                    "max": 50,
                    "used": 1,
                    "list_routers": [
                                {
                                    "router_id": "router01",
                                    "is_gateway": False
                                }
                    ]
                  }

        return routers

    def get_internet_gateways(self):
        internet_gateways = {
                              "max": 5,
                              "used": 1,
                              "list_internet_gateways": [
                                  {"internet_gateway_id": "igw01"}
                              ]
                            }

        return internet_gateways

    def get_vpn_gateways(self):
        vpn_gateways = {
                          "max": 5,
                          "used": 1,
                          "list_vpn_gateways": [
                                              {
                                                  "vpn_gateway_id": "vnp01",
                                                  "max_connections": 10,
                                                  "used_connections": 1,
                                                  "list_connections": []
                                              }
                          ]
                        }

        return vpn_gateways

    def get_firewall(self):
        firewall = {
                      "max": 50,
                      "used": 1,
                      "list_firewalls": [
                                      {
                                          "firewall_id": "fw01",
                                          "rules_max": 50,
                                          "rules_used": 10,
                                          "list_rules": []
                                      }
                      ]
                    }

        return firewall

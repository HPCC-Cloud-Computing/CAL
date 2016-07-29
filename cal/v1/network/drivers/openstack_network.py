""" OpenstackDriver for Network
    based on NetworkDriver
"""

from neutronclient.v2_0 import client
from network_driver import NetworkDriver


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

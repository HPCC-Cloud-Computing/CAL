""" OpenstackDriver for Network
    based on NetworkDriver
"""


from keystoneauth1.identity import v3
from keystoneauth1 import session
from neutronclient.v2_0 import client
from cal.v1.network.drivers.network_driver import NetworkDriver, NetworkQuota


class OpenstackNetWorkDriver(NetworkDriver):
    """docstring for OpenstackNetWorkDriver"""

    def __init__(self, auth_url, project_name,
                 username, password, **kargs):
        super(OpenstackNetWorkDriver, self).__init__()
        self.provider = "OPENSTACK"
        self.auth_url = auth_url
        self.project_name = project_name
        self.username = username
        self.password = password
        self.user_domain_name = kargs.pop('user_domain_name', 'default')
        self.project_domain_name = kargs.pop('project_domain_name', 'default')
        self.driver_name = kargs.pop('driver_name', 'default')
        self._setup()

    def _setup(self):
        auth = v3.Password(auth_url=self.auth_url,
                           user_domain_name=self.user_domain_name,
                           username=self.username,
                           password=self.password,
                           project_domain_name=self.project_domain_name,
                           project_name=self.project_name)
        sess = session.Session(auth=auth)
        self.client = client.Client(session=sess)
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
                  'gateway_ip': subnet['gateway_ip'],
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
        subnets = self.client.list_subnets().get('subnets')
        list_cidrs = []
        for subnet in subnets:
            list_cidrs.append({"net_id": subnet['id'],
                               "cidr": "{}".format(subnet['cidr'])})
        networks = {
            "max": 50,
            "used": len(list_cidrs),
            "list_cidrs": list_cidrs,
            "VPCs": None
        }

        return networks

    def get_security_groups(self):
        tenant_id = self.client.get_quotas_tenant().get('tenant')['tenant_id']
        list_security_groups = self.client.list_security_groups(
            tenant_id=tenant_id).get('security_groups')
        list_scgs = []
        for scg in list_security_groups:
            list_scgs.append({
                "security_group_id": scg['id'],
                "rules_max": 50,
                "rules_used": len(scg['security_group_rules']),
                "list_rules": scg['security_group_rules']
            })
        security_groups = {
            "max": 50,
            "used": len(list_security_groups),
            "list_security_groups": list_scgs
        }
        return security_groups

    def get_floating_ips(self):
        ips = self.client.list_floatingips().get('floatingips')
        list_ips = []
        for ip in ips:
            list_ips.append(ip['floating_ip_address'])
        floating_ips = {
            "max": 255,
            "used": len(list_ips),
            "list_floating_ips": list_ips
        }

        return floating_ips

    def get_routers(self):
        rts = self.client.list_routers().get('routers')
        list_routers = []
        for router in rts:
            list_routers.append({
                "router_id": router['id'],
                "is_gateway": True
            })
        routers = {
            "max": 50,
            "used": len(list_routers),
            "list_routers": list_routers
        }

        return routers

    def get_internet_gateways(self):
        # internet_gateways = {
        #     "max": 5,
        #     "used": 1,
        #     "list_internet_gateways": [
        #         {"internet_gateway_id": "igw01"}
        #     ]
        # }
        pass

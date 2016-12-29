""" AmazonDriver for Network
    based on BaseDriver
"""


import boto3

from calplus.v1.network.drivers.base import BaseDriver, BaseQuota


PROVIDER = "AMAZON"


class AmazonDriver(BaseDriver):

    """docstring for AmazonDriver"""

    def __init__(self, cloud_config):
        super(AmazonDriver, self).__init__()
        self.aws_access_key_id = cloud_config['aws_access_key_id']
        self.aws_secret_access_key = cloud_config['aws_secret_access_key']
        self.endpoint_url = cloud_config['endpoint_url']
        self.region_name = cloud_config.get('region_name', None)
        self.driver_name = \
            cloud_config.get('driver_name', 'default')
        self.limit = cloud_config.get('limit', None)
        self._setup()

    def _setup(self):
        self.client = boto3.client(
            'ec2',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        )
        self.quota = None

    def _get_or_create_gateway(self):
        gateways = self.client.describe_internet_gateways()['InternetGateways']
        for gateway in gateways:
            if not gateway.get('Attachments'):
                return gateway

        return self.client.create_internet_gateway().get('InternetGateway')

    def _add_route_to_allow_subnet_connect_internet(self, vpc_id, subnet_id):

        gateways = self.client.describe_internet_gateways(
            Filters=[{
                'Name': 'attachment.vpc-id',
                'Values': [
                    vpc_id,
                ]
            }]
        )
        gateway_id = gateways.get('InternetGateways')[0]['InternetGatewayId']

        routetables = self.client.describe_route_tables(
            Filters=[{
                'Name': 'vpc-id',
                'Values': [
                    vpc_id,
                ]
            }]
        )
        route_id = routetables.get('RouteTables')[0].get('RouteTableId')

        self.client.associate_route_table(
            RouteTableId=route_id,
            SubnetId=subnet_id
        )

        self.client.create_route(
            RouteTableId=route_id,
            GatewayId=gateway_id,
            DestinationCidrBlock='0.0.0.0/0'
        )

        return True

    def create(self, name, cidr, **kargs):

        # step1: create vpc
        vpc = self.client.create_vpc(
            CidrBlock=cidr,
            InstanceTenancy='default'
        ).get('Vpc')
        # step 2: create subnet
        subnet = self.client.create_subnet(
            VpcId=vpc.get('VpcId'),
            CidrBlock=cidr
        ).get('Subnet')

        # TODO: this is teriable thing. we should develop
        # sg manage in compute driver ASAP
        group_id = self.client.describe_security_groups(
            Filters=[{
                'Name': 'vpc-id',
                'Values': [vpc.get('VpcId')]
            }]).get('SecurityGroups')[0].get('GroupId')
        self.client.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=[{
                'ToPort': 65534,
                'IpProtocol': 'tcp',
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
                'FromPort': 1
            }])

        dhcp = self.client.create_dhcp_options(
            DhcpConfigurations=[{
                'Key': 'domain-name-servers',
                'Values': ['8.8.8.8', '8.8.4.4']},
            ]).get('DhcpOptions')
        self.client.associate_dhcp_options(
            DhcpOptionsId=dhcp.get('DhcpOptionsId'),
            VpcId=vpc.get('VpcId')
        )

        result = {'name': subnet['SubnetId'],
                  'description': None,
                  'id': subnet['SubnetId'],
                  'cidr': subnet['CidrBlock'],
                  'cloud': PROVIDER,
                  'gateway_ip': None,
                  'security_group': None,
                  'allocation_pools': None,
                  'dns_nameservers': None,
                  'network_id': subnet['VpcId']
                  }

        return result

    def show(self, subnet_id):
        subnet = self.client.describe_subnets(
            SubnetIds=[subnet_id]).get('Subnets')[0]

        result = {'name': subnet['SubnetId'],
                  'description': None,
                  'id': subnet['SubnetId'],
                  'cidr': subnet['CidrBlock'],
                  'cloud': PROVIDER,
                  'gateway_ip': None,
                  'security_group': None,
                  'allocation_pools': None,
                  'dns_nameservers': None,
                  'network_id': subnet['VpcId']
                  }

        return result

    def list(self, **search_opts):
        subnets = self.client.describe_subnets(**search_opts).get('Subnets')
        result = []
        for subnet in subnets:
            sub = {'name': subnet['SubnetId'],
                   'description': None,
                   'id': subnet['SubnetId'],
                   'cidr': subnet['CidrBlock'],
                   'cloud': PROVIDER,
                   'gateway_ip': None,
                   'security_group': None,
                   'allocation_pools': None,
                   'dns_nameservers': None,
                   'network_id': subnet['VpcId']
                   }
            result.append(sub)

        return result

    def update(self, subnet_id, subnet):
        pass

    def delete(self, subnet_id):
        """
        This is bad delete function
        because one vpc can have more than one subnet.
        It is Ok if user only use CAL for manage cloud resource
        We will update ASAP.
        """
        # 1 : show subnet
        subnet = self.client.describe_subnets(
            SubnetIds=[subnet_id]).get('Subnets')[0]
        vpc_id = subnet.get('VpcId')
        # 2 : delete subnet
        self.client.delete_subnet(SubnetId=subnet_id)
        # 3 : delete vpc
        return self.client.delete_vpc(VpcId=vpc_id)

    def connect_external_net(self, subnet_id):
        # 1: get subnet to get VpcId
        subnet = self.show(subnet_id)
        # 2: get free gateway or create it
        gateway = self._get_or_create_gateway()
        # 3: attach Vpc - gateway
        self.client.attach_internet_gateway(
            InternetGatewayId=gateway.get('InternetGatewayId'),
            VpcId=subnet.get('network_id')
        )
        # 4: associate routetable with subnet
        # add new route to route table inside Vpc
        self._add_route_to_allow_subnet_connect_internet(
            subnet.get('network_id'),
            subnet_id
        )

        return gateway.get('InternetGatewayId')

    def disconnect_external_net(self, gateway_id, subnet_id):
        subnet = self.show(subnet_id)
        self.client.detach_internet_gateway(
            InternetGatewayId=gateway_id,
            VpcId=subnet.get('network_id')
        )
        return True

    def allocate_public_ip(self):
        ip = self.client.allocate_address(Domain='vpc')
        return {
                'public_ip': ip.get('PublicIp'),
                'id': ip.get('AllocationId')
        }

    def list_public_ip(self, **search_opts):
        """

        :param search_opts:
        :return: list PublicIP
        """
        result = self.client.describe_addresses(**search_opts)
        ips = result.get('Addresses')
        return_format = []
        for ip in ips:
            return_format.append({
                'public_ip': ip.get('PublicIp'),
                'id': ip.get('AllocationId')
            })
        return return_format

    def release_public_ip(self, public_ip_id):
        self.client.release_address(AllocationId=public_ip_id)
        return True


class AmazonQuota(BaseQuota):

    """docstring for AmazonQuota"""

    def __init__(self, client, limit=None):
        super(AmazonQuota, self).__init__()
        self.client = client
        self.limit = limit
        self._setup()

    def _setup(self):
        if self.limit is None:
            self.limit = None

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

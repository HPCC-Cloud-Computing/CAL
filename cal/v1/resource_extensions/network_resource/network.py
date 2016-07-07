from validate import *

class NetworkController(object):

    # Define support for GET on a collection
    @validate_driver
    def index(self, req, driver):
        """List all network
        List all of netowrks on special cloud
        with:
        :Param  req
        :Type   object Request
        """
    	result = driver.list_network(req.params) # some filter, ...
        data = {
            'action': "index",
            'controller': "network",
            'cloud': req.environ['cal.cloud']
            'result': result
        }
        return data

    def delete(self, req, id):
        """Delete a network
        Delete a specific netowrk with id on special cloud
        with:
        :Param  req
        :Type   object Request
        """
        response = driver.delete_network(req.params,id) # some filter, ...
        data = {
            'action': "delete",
            'controller': "network",
            'id': id,
            'cloud': req.environ['cal.cloud'],
            'response': response
        }
        return data

    def update(self, req, id):
        """Update a network
        Update a specific netowrk with id on special cloud
        with:
        :Param  req
        :Type   object Request
        """
        response = driver.update_network(req.params,id) # some filter, ...
        data = {
            'action': "update",
            'controller': "network",
            'id': id,
            'cloud': req.environ['cal.cloud'],
            'response': response
        }
        return data

    @validate_driver
    @validate_resource
    def create(self, req, driver):
        """Create a network
        Create a new netowrk on special cloud
        with:
        :Param  req
        :Type   object Request
        """
        response = driver.create_network(req.params) # name, CIRD, pool
        data = {
            'action': "create",
            'controller': "network",
            'cloud': req.environ['cal.cloud']
            'response': response #metadata of network 
        }
        return data

    def get(self, req, id):
        """Get info of a network
        Get info of a specific netowrk with id on special cloud
        with:
        :Param  req
        :Type   object Request
        """
        response = driver.get_network(req.params,id) # some filter, ...
        data = {
            'action': "get",
            'controller': "network",
            'id': id,
            'cloud': req.environ['cal.cloud'],
            'response': response
        }
        return data


    def detail(self, req):
        data = {
            'action': 'detail',
            'controller': 'network',
            'cloud': req.environ['cal.cloud']
        }
        return data

    # def mem_action(self, req, id):
    #     data = {
    #         'action': 'mem_action',
    #         'controller': 'basic',
    #         'id': id,
    #         'cloud': req.environ['cal.cloud']
    #     }
    #     return data

    def attach_igw(self, req, id):
        """Attach network to Internet gateway
        :Param  req
        :Type   object Request
        """       
        igw = driver.get_igw(req.params)
        if igw is None:
            igw = driver.create_igw(req.params)
        response = driver.attach_igw(req.params,igw)
        data = {
            'action': 'attach_igw',
            'controller': 'network',
            'id': id,
            'cloud': req.environ['cal.cloud']
            'response': response
        }
        return data
    def dettach_igw(self, req, id):
        """Dettach network from Internet gateway
        :Param  req
        :Type   object Request
        """       
        response = driver.dettach_igw(req.params)
        data = {
            'action': 'attach_igw',
            'controller': 'network',
            'id': id,
            'cloud': req.environ['cal.cloud']
            'response': response
        }
        return data

    def attach_vpngw(self, req, id):
        """Attach network to VPN gateway
        :Param  req
        :Type   object Request
        """       
        vpngw = driver.get_vnpgw(req.params,id)
        if vpngw is None:
            vpngw = driver.create_vpngw(req.params,id)
        response = driver.attach_vpngw(req.params,vpngw)
        data = {
            'action': 'attach_igw',
            'controller': 'network',
            'id': id,
            'cloud': req.environ['cal.cloud']
            'response': response
        }
        return data

    def dettach_vpngw(self, req, id):
        """Dettach network from Internet gateway
        :Param  req
        :Type   object Request
        """       
        response = driver.dettach_vpngw(req.params)
        data = {
            'action': 'attach_igw',
            'controller': 'network',
            'id': id,
            'cloud': req.environ['cal.cloud']
            'response': response
        }
        return data

    def add_firewall(self, req, id):
        pass

    def remove_firewall(self, req, id):
        pass

class Network:
    collection_name = 'network'
    member_name = 'network'
    controller = NetworkController()
    parent_resource = {}
    collection = {'detail': 'GET'}
    member = {'attach_igw': 'POST', 'dettach_igw': 'POST', 'attach_vpngw': 'POST', 'dettach_vpngw': 'POST'}
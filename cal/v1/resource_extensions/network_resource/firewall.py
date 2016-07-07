from validate import *

class FirewallController(object):

    # Define support for GET on a collection
    @validate_driver
    def index(self, req, driver):
        """List all firewall
        List all of firewalls on special cloud
        with:
        :Param  req
        :Type   object Request
        """
    	result = driver.list_firewall(req.params) # some filter, ...
        data = {
            'action': "index",
            'controller': "firewall",
            'cloud': req.environ['cal.cloud']
            'result': result
        }
        return data

    def delete(self, req, id):
        """Delete a firewall
        Delete a specific netowrk with id on special cloud
        with:
        :Param  req
        :Type   object Request
        """
        response = driver.delete_firewall(req.params,id) # some filter, ...
        data = {
            'action': "delete",
            'controller': "firewall",
            'id': id,
            'cloud': req.environ['cal.cloud'],
            'response': response
        }
        return data

    def update(self, req, id):
        """Update a firewall
        Update a specific netowrk with id on special cloud
        with:
        :Param  req
        :Type   object Request
        """
        response = driver.update_firewall(req.params,id) # some filter, ...
        data = {
            'action': "update",
            'controller': "firewall",
            'id': id,
            'cloud': req.environ['cal.cloud'],
            'response': response
        }
        return data

    @validate_driver
    @validate_resource
    def create(self, req, driver):
        """Create a firewall
        Create a new netowrk on special cloud
        with:
        :Param  req
        :Type   object Request
        """
        response = driver.create_firewall(req.params)
        data = {
            'action': "create",
            'controller': "firewall",
            'cloud': req.environ['cal.cloud']
            'response': response #metadata of firewall 
        }
        return data

    def get(self, req, id):
        """Get info of a firewall
        Get info of a specific firewall with id on special cloud
        with:
        :Param  req
        :Type   object Request
        """
        response = driver.get_firewall(req.params,id) # some filter, ...
        data = {
            'action': "get",
            'controller': "firewall",
            'id': id,
            'cloud': req.environ['cal.cloud'],
            'response': response
        }
        return data


    def detail(self, req):
        data = {
            'action': 'detail',
            'controller': 'firewall',
            'cloud': req.environ['cal.cloud']
        }
        return data

class firewall:
    collection_name = 'firewall'
    member_name = 'firewall'
    controller = firewallController()
    parent_resource = {}
    collection = {'detail': 'GET'}
    member = {'add_rule':'POST', 'delete_rule':'POST', 'update_rule':'POST'}
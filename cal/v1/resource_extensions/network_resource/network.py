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
        data = {
            'action': "delete",
            'controller': "basic",
            'id': id,
            'cloud': req.environ['cal.cloud']
        }
        return data

    def update(self, req, id):
        data = {
            'action': "update",
            'controller': "basic",
            'id': id,
            'cloud': req.environ['cal.cloud']
        }
        return data

    @validate_driver
    @validate_resource
    def create(self, req, driver):
        result = driver.create_network(req.params) # name, CIRD, pool
        data = {
            'action': "create",
            'controller': "basic",
            'cloud': req.environ['cal.cloud']
            'result': result
        }
        return data

    def show(self, req, id):
        data = {
            'action': "show",
            'controller': "basic",
            'id': id,
            'cloud': req.environ['cal.cloud']
        }
        return data


    def detail(self, req):
        data = {
            'action': 'detail',
            'controller': 'basic',
            'cloud': req.environ['cal.cloud']
        }
        return data

    def mem_action(self, req, id):
        data = {
            'action': 'mem_action',
            'controller': 'basic',
            'id': id,
            'cloud': req.environ['cal.cloud']
        }
        return data

class Network:
    collection_name = 'network'
    member_name = 'network'
    controller = NetworkController()
    parent_resource = {}
    collection = {'detail': 'GET'}
    member = {'mem_action': 'GET'}
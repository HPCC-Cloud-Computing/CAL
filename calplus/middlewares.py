from oslo_context import context

from calplus import base
from calplus import utils


class DeserializeMiddleware(base.BaseMiddleware):

    def __init__(self):
        super(DeserializeMiddleware, self).__init__()

    def _deserialize(self, req):
        deserializer = utils.JSONRequestDeserializer()
        body = deserializer.default(req)
        cloud = body['body']['cloud']
        req.env['calplus.cloud'] = str(cloud)

    def __attach_req_id_to_resp(self, req, resp):
        req_id = context.generate_request_id()
        req.env['request-id'] = req_id
        if 'x-request-id' not in resp._headers:
            resp._headers['x-request-id'] = req_id

    def process_request(self, req, resp):
        self._deserialize(req)
        self.__attach_req_id_to_resp(req, resp)


class FuncMiddleware(base.BaseMiddleware):

    def __init__(self, func):
        super(FuncMiddleware, self).__init__()
        self.func = func

    def process_resource(self, req, resp, resource, params):
        return self.func(req, resp, resource, params)


class SerializeMiddleware(base.BaseMiddleware):

    def __init__(self):
        super(SerializeMiddleware, self).__init__()

    def _serialize(self, resp, result):
        serializer = utils.JSONResponseSerializer()
        serializer.default(resp, result)

    def process_response(self, req, resp, resource):
        self._serialize(resp, resp.body)

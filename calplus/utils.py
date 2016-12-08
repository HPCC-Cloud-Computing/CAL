import datetime
try:
    import simplejson as json
except ImportError:
    import json

import falcon
from falcon import Response
from oslo_config import cfg

import calplus.conf
from calplus.provider import Provider

CONF = calplus.conf.CONF


class JSONRequestDeserializer(object):

    def has_body(self, request):
        if 'transfer-encoding' in request.headers:
            return True
        elif request.content_length > 0:
            return True

        return False

    def _sanitizer(self, obj):
        """Sanitizer method that will be passed to json.loads."""
        return obj

    def from_json(self, datastring):
        try:
            return json.loads(datastring, object_hook=self._sanitizer)
        except ValueError:
            msg = 'Malformed JSON in request body.'
            raise falcon.HTTPBadRequest(
                title='Malformed JSON', description=msg)

    def default(self, request):
        if self.has_body(request):
            body = request.stream.read(request.content_length)
            return {'body': self.from_json(body.decode("utf-8"))}
        else:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON doc is required')


class JSONResponseSerializer(object):

    def _sanitizer(self, obj):
        """Sanitizer method that will be passed to json.dumps."""
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return obj

    def to_json(self, data):
        return json.dumps(data, default=self._sanitizer, sort_keys=True)

    def default(self, response, result):
        response.content_type = 'application/json'
        response.body = self.to_json(result)


def append_request_id(req, resp, resource, params):
    """Append request id which got from response
    header to resource.req_ids list.
    """
    def get_headers(resp):
        if hasattr(resp, 'headers'):
            return resp.headers
        if hasattr(resp, '_headers'):
            return resp._headers
        return None

    if(isinstance(resp, Response) or
       (get_headers(resp) is not None)):
        # Extract 'x-request-id' from headers if
        # response is a Response object.
        request_id = get_headers(resp).get('x-request-id')
    else:
        # If resp is of type string or None.
        request_id = resp

    if resource.req_ids is None:
        resource.req_ids = []

    if request_id not in resource.req_ids:
        resource.req_ids.append(request_id)


def set_config_file(file_path):
    CONF(['--config-file', file_path])


def get_list_providers():
    # ensure all driver groups have been registered
    sections = CONF.list_all_sections()
    for section in sections:
        CONF.register_group(cfg.OptGroup(section))

    # ensure all of enable drivers configured exact opts
    enable_drivers = CONF.providers.enable_drivers
    list_providers = []
    for driver in enable_drivers.keys():
        type_driver = enable_drivers.get(driver)
        if type_driver == 'openstack':
            CONF.register_opts(
                calplus.conf.providers.openstack_opts, driver)
        elif type_driver == 'amazon':
            CONF.register_opts(
                calplus.conf.providers.amazon_opts, driver)
        else:
            continue
        list_providers.append(
            Provider(type_driver, CONF.get(driver))
        )

    return list_providers

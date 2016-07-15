"""
Test WSGI basics and provide some helper functions for other WSGI tests.
"""

import falcon

from cal.tests import base
from cal import base as wsgi_base
from cal import wsgi


def _first_hook(req, resp, resource):
    if not req.client_accepts_json:
        raise falcon.HTTPNotAcceptable(
            'This API only supports responses encoded as JSON.',
            href='http://docs.examples.com/api/json')

    if req.method in ('POST', 'PUT'):
        if 'application/json' not in req.content_type:
            raise falcon.HTTPUnsupportedMediaType(
                'This API only supports requests encoded as JSON.',
                href='http://docs.examples.com/api/json')


def _second_hook(req, resp, resource):
    headers = req.headers
    methods = headers.get('URL-METHODS', '').split(',')

    if req.method not in methods:
        raise falcon.HTTPNotFound()


class TestController(object):

    def get(self, msg):
        return msg


class TestResource(wsgi_base.BaseSource):

    def __init__(self, controller):
        self.controller = controller

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.controller.get('Success')


class TestWSGIDriver(wsgi.WSGIDriver):

    def __init__(self):
        super(TestWSGIDriver, self).__init__()

    def before_hooks(self):
        return [
            _first_hook,
            _second_hook,
        ]

    def _init_routes_and_middlewares(self):
        middleware = \
                [wsgi.FuncMiddleware(hook) for hook in self.before_hooks()]
        self.app = falcon.API(middleware=middleware)

        controller = TestController()
        self.app.add_route('/', TestResource(controller))


class Test(base.TestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.wsgi_driver = TestWSGIDriver()
        self.api = self.wsgi_driver.app

    def test_first_hook_raise_HTTPNotAcceptable(self):
        bad_headers = {
            'Accept': 'application/xml',
        }

        result = self.simulate_get(path='/', headers=bad_headers)
        self.assertEqual(falcon.HTTP_406, result.status)

    def test_first_hook_raise_HTTPUnsupportedMediaType(self):
        bad_headers = {
            'Content-Type': 'text/html',
            'URL-METHODS': 'POST, GET, PUT',
        }

        result = self.simulate_post(path='/', headers=bad_headers)
        self.assertEqual(falcon.HTTP_415, result.status)

    def test_second_hook_raise_HTTPNotFound(self):
        headers = {
            'Content-Type': 'application/json',
            'URL-METHODS': 'GET, PUT',
        }
        result = self.simulate_post(path='/', headers=headers)
        self.assertEqual(falcon.HTTP_404, result.status)

    def test_pass_all_hooks(self):
        headers = {
            'Content-Type': 'application/json',
            'URL-METHODS': 'POST, GET, PUT',
        }
        result = self.simulate_post(path='/', headers=headers)
        self.assertEqual(falcon.HTTP_200, result.status)

    def test_wrong_router(self):
        result = self.simulate_get(path='/some/wrong/path')
        self.assertEqual(falcon.HTTP_404, result.status)
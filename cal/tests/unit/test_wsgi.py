"""
Test WSGI basics and provide some helper functions for other WSGI tests.
"""

import routes
import webob
import webob.exc

from cal import wsgi
from cal.tests import base


class Test(base.NoDBTestCase):

    def test_debug(self):

        class Application(wsgi.Application):
            """Dummy application to test debug."""

            def __call__(self, environ, start_response):
                start_response("200", [("X-Test", "checking")])
                return ['Test result']

        application = wsgi.Debug(Application())
        result = webob.Request.blank('/').get_response(application)
        self.assertEqual(result.body, "Test result")

    def test_router(self):

        class Application(wsgi.Application):
            """Test application to call from router."""

            def __call__(self, environ, start_response):
                start_response("200", [])
                return ['Router result']

        class Router(wsgi.Router):
            """Test router."""

            def __init__(self):
                mapper = routes.Mapper()
                mapper.connect("/test", controller=Application())
                super(Router, self).__init__(mapper)

        result = webob.Request.blank('/test').get_response(Router())
        self.assertEqual(result.body, "Router result")
        result = webob.Request.blank('/bad').get_response(Router())
        self.assertNotEqual(result.body, "Router result")


class JSONRequestDeserializerTest(base.NoDBTestCase):

    def setUp(self):
        super(JSONRequestDeserializerTest, self).setUp()
        self.deserializer = wsgi.JSONRequestDeserializer()

    def test_has_body_return_false(self):
        request = wsgi.Request.blank(
            "/", headers={'Content-Length': 0})

        self.assertFalse(self.deserializer.has_body(request))

    def test_has_body_return_true(self):
        request = wsgi.Request.blank(
            "/", headers={'Content-Length': 1})

        self.assertTrue(self.deserializer.has_body(request))

    def test_default_with_has_body_return_false(self):
        request = wsgi.Request.blank(
            "/", headers={'Content-Length': 0})

        self.assertEqual({},
                         self.deserializer.default(request))

    def test_default_success(self):
        data = """{"a": {
                "a1": "1",
                "a2": "2",
                "bs": ["1", "2", "3", {"c": {"c1": "1"}}],
                "d": {"e": "1"},
                "f": "1"}}"""

        as_dict = {
            'body': {
                u'a': {
                    u'a1': u'1',
                    u'a2': u'2',
                    u'bs': [u'1', u'2', u'3', {u'c': {u'c1': u'1'}}],
                    u'd': {u'e': u'1'},
                    u'f': u'1'}}}

        request = webob.Request.blank("/", body=data)

        self.assertEqual(as_dict,
                         self.deserializer.default(request))

    def test_default_raise_Malformed_Exception(self):
        request = wsgi.Request.blank("/", body=b"{mal:formed")

        self.assertRaises(
            webob.exc.HTTPBadRequest,
            self.deserializer.default,
            request)


class JSONResponseSerializerTest(base.NoDBTestCase):

    def setUp(self):
        super(JSONResponseSerializerTest, self).setUp()
        self.serializer = wsgi.JSONResponseSerializer()

    def test_default(self):
        result = {
            'a': {
                'a1': '1',
                'a2': '2',
                'bs': ['1', '2', '3', {'c': {'c1': '1'}}],
                'd': {'e': '1'},
                'f': '1'}
        }

        expected_body = '{"a": {"a1": "1", "a2": "2", ' \
                        '"bs": ["1", "2", "3", ' \
                        '{"c": {"c1": "1"}}], '\
                        '"d": {"e": "1"}, "f": "1"}}'

        response = webob.Response()
        self.serializer.default(response, result)
        self.assertEqual("application/json",
                         response.content_type)
        self.assertEqual(response.body, expected_body)


class ResouceTest(base.NoDBTestCase):

    def setUp(self):
        super(ResouceTest, self).setUp()
        self.resource = wsgi.Resource(self.Controller())

    class Controller(object):
        def index(self, req, index=None):
            return index

    def test_dispatch(self):
        actual = self.resource.dispatch(self.resource.controller, 'index',
                                        None, 'off')
        expected = 'off'
        self.assertEqual(actual, expected)

    def test_dispatch_unknown_action(self):
        self.assertRaises(
            AttributeError, self.resource.dispatch,
            self.resource.controller, 'create', {})

    def test_get_action_args(self):
        env = {
            'wsgiorg.routing_args': [None, {
                'controller': None,
                'format': None,
                'action': 'update',
                'id': 12,
            }],
        }

        expected = {'action': 'update', 'id': 12}

        self.assertEqual(self.resource.get_action_args(env),
                         expected)

    # def test_malformed_request_body_throws_bad_request(self):
    #     resource = wsgi.Resource(None)
    #     request = wsgi.Request.blank(
    #         "/", body=b"{mal:formed", method='POST',
    #         headers={'Content-Type': "application/json"})

    #     response = resource(request)
    #     self.assertEqual(400, response.status_int)

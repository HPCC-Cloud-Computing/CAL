"""Hello World using Paste + WSGI """
from paste import httpserver


def application(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    return ['Hello World']


httpserver.serve(application, host='0.0.0.0', port=8080)
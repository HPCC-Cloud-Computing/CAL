from paste import httpserver
from paste.deploy import loadapp


INI_PATH = '/home/techbk/Projects/CAL/cal/cal-paste.ini'

wsgi_app = loadapp('config:' + INI_PATH, name='cal')
httpserver.serve(wsgi_app, host='0.0.0.0', port=8080)
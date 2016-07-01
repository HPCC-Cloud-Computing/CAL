# from paste import httpserver
from paste.deploy import loadapp
import os
from werkzeug import serving


# INI_PATH = "config:{}".format(os.path.abspath("cal-paste.ini"))
INI_PATH = "config:{}".format("/home/techbk/Projects/CAL/cal/cal-paste.ini")

wsgi_app = loadapp(INI_PATH, name='cal')

if __name__=='__main__':
    serving.run_simple('0.0.0.0', 8080, wsgi_app)
# httpserver.serve(wsgi_app, host='0.0.0.0', port=8080)
"""WSGI App for WSGI Containers
This app should be used by external WSGI
containers. For example:
    $ gunicorn cal.app:app
NOTE: As for external containers, it is necessary
to put config files in the standard paths. There's
no common way to specify / pass configuration files
to the WSGI app when it is called from other apps.
"""

from oslo_config import cfg

from cal.wsgi import WSGIDriver

conf = cfg.CONF

wsgi_driver = WSGIDriver()
app = wsgi_driver.app

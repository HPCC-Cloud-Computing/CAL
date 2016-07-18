from oslo_config import cfg
from oslo_log import log as logging

from cal import wsgi

CONF = cfg.CONF


def run():
    wsgi_driver = wsgi.WSGIDriver()
    wsgi_driver.listen()

if __name__ == '__main__':
    run()
    logging.setup(CONF, 'cal')

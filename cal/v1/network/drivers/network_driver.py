""" this is contain abstract Class
for all network driver which we want to implement
"""
"""NetworkDriver abstract
"""


class NetworkDriver(object):

    """abstract class for network driver"""

    def __init__(self):
        super(NetworkDriver, self).__init__()
        self.provider = "Unknown"

    def create():
        raise NotImplementedError

    def show():
        raise NotImplementedError

    def list():
        raise NotImplementedError

    def update():
        raise NotImplementedError

    def delete():
        raise NotImplementedError

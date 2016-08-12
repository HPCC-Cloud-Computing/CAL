from cal.base import BaseClient


class Client(BaseClient):
    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""

    def __init__(self, provider, *args, **kwargs):
        _path = 'cal.v1.object_storage.driver'
        BaseClient.__init__(self, _path, provider)

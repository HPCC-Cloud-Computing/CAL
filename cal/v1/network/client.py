from cal.base import BaseClient


class Client(BaseClient):
    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""

    def __init__(self, provider, *args, **kwargs):
        _path = 'cal.v1.network.driver'
        BaseClient.__init__(self, _path, provider)

    def create_network(self, name, *args, **kwargs):
        self.driver.create_network(name, *args, **kwargs)

    def delete_network(self, id):
        self.driver.delete_network(id)

    def list_network(self):
        self.driver.list_network()

    def show_network(self, id):
        self.driver.show_network(id)

    def update_network(self, id):
        self.driver.update_network(id)

    def attach_to_router(self):
        self.driver.attach_to_router()

    def detach_to_router(self):
        self.driver.detach_to_router()

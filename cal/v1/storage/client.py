from cal import base


class Client(base.Singleton):
    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""
    pass

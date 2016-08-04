"""
Exception definitions
"""


class UnsupportedVersion(Exception):
    """Indicates that the user is trying to use an UnsupportedVersion
    version of the API.
    """
    pass


class EndpointNotFound(Exception):
    """Could not find Service or Region in Service Catalog."""
    pass


class ConnectionRefused(Exception):
    """
    Connection refused: the server refused the connection.
    """
    def __init__(self, response=None):
        self.response = response

    def __str__(self):
        return "ConnectionRefused: %s" % repr(self.response)

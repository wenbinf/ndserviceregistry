class ServiceRegistryException(Exception):

    """ServiceParty Exception Object"""

    def __init__(self, e):
        self.value = e

    def __str__(self):
        return self.value

class NoConnection(ServiceRegistryException):
    """Any time the backend service is unavailable for an action."""

class ReadOnly(ServiceRegistryException):
    """Thrown when a Write operation is attempted while in Read Only mode."""


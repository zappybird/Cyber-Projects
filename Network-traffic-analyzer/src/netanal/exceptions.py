class NetAnalError(Exception):
    """Base exception for the analyzer."""

class PermissionError(NetAnalError):
    pass

class InvalidFilterError(NetAnalError):
    pass

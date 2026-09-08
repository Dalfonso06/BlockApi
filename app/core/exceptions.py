class NotFoundError(Exception):
    """A requested resource does not exist."""


class PermissionDeniedError(Exception):
    """The caller is authenticated but not authorized to act on this resource."""


class ConflictError(Exception):
    """The operation conflicts with existing state (uniqueness violation, FK-RESTRICT in use)."""

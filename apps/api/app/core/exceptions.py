class PolyHistoryException(Exception):
    """Base exception for PolyHistory API."""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(PolyHistoryException):
    """Resource not found."""
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, status_code=404)


class ValidationException(PolyHistoryException):
    """Validation error."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=422, details=details)


class AuthenticationException(PolyHistoryException):
    """Authentication error."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationException(PolyHistoryException):
    """Authorization error."""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, status_code=403)


class InsufficientBalanceException(PolyHistoryException):
    """Monthly analysis limit exceeded."""
    def __init__(self, limit: int):
        super().__init__(
            f"Monthly analysis limit ({limit}) exceeded. Upgrade your plan.",
            status_code=429
        )


class JudgeTimeoutException(PolyHistoryException):
    """Model judge timeout."""
    def __init__(self, model_name: str):
        super().__init__(
            f"Model {model_name} timed out",
            status_code=504
        )


class InsufficientConsensusException(PolyHistoryException):
    """Not enough models responded for consensus."""
    def __init__(self, successful: int, required: int):
        super().__init__(
            f"Only {successful} models succeeded, minimum {required} required",
            status_code=503
        )

class AIException(Exception):
    """Base exception for all AI platform errors."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ProviderException(AIException):
    """Exception raised when an AI provider returns an error."""
    def __init__(self, message: str, provider: str, status_code: int = 502):
        super().__init__(f"Provider '{provider}' error: {message}", status_code)
        self.provider = provider


class ModelRouteException(AIException):
    """Exception raised when model routing fails."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)


class RateLimitException(AIException):
    """Exception raised when provider rate limits are exceeded."""
    def __init__(self, message: str, provider: str, status_code: int = 429):
        super().__init__(f"Rate limit exceeded for provider '{provider}': {message}", status_code)
        self.provider = provider


class InvalidRequestException(AIException):
    """Exception raised when request contracts are violated."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)

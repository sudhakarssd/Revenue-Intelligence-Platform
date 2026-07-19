import pytest
from app.ai.exceptions.exceptions import (
    AIException,
    ProviderException,
    ModelRouteException,
    RateLimitException,
    InvalidRequestException,
)


def test_exceptions_properties():
    # Test base AIException
    ex = AIException("generic error", status_code=500)
    assert ex.message == "generic error"
    assert ex.status_code == 500
    
    # Test ProviderException
    ex_p = ProviderException("connection failed", provider="openai")
    assert "Provider 'openai' error: connection failed" in ex_p.message
    assert ex_p.provider == "openai"
    assert ex_p.status_code == 502
    
    # Test ModelRouteException
    ex_r = ModelRouteException("routing failure")
    assert ex_r.message == "routing failure"
    assert ex_r.status_code == 400
    
    # Test RateLimitException
    ex_rl = RateLimitException("quota exceeded", provider="openai")
    assert "Rate limit exceeded for provider 'openai': quota exceeded" in ex_rl.message
    assert ex_rl.provider == "openai"
    assert ex_rl.status_code == 429
    
    # Test InvalidRequestException
    ex_ir = InvalidRequestException("bad payload")
    assert ex_ir.message == "bad payload"
    assert ex_ir.status_code == 400

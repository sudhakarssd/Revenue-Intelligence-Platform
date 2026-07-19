import pytest
from app.ai.providers.factory import ProviderFactory
from app.shared.enums import ProviderType


def test_provider_factory_get_success():
    factory = ProviderFactory()
    provider = factory.get_provider(ProviderType.OPENAI)
    assert provider is not None
    
    # Retrieve provider using case-insensitive string name
    provider_str = factory.get_provider("openai")
    assert provider_str is not None
    assert provider_str == provider


def test_provider_factory_unsupported_string():
    factory = ProviderFactory()
    with pytest.raises(ValueError) as exc_info:
        factory.get_provider("unsupported-mock-provider")
    assert "Unsupported AI Provider" in str(exc_info.value)


def test_provider_factory_unregistered_enum():
    factory = ProviderFactory()
    # GEMINI is declared in ProviderType but has no implementation registered in Phase 1
    with pytest.raises(ValueError) as exc_info:
        factory.get_provider(ProviderType.GEMINI)
    assert "is not registered" in str(exc_info.value)

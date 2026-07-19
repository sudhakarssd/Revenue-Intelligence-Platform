from typing import Dict, Union
from app.ai.providers.base import BaseAIProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.infrastructure.config import settings
from app.shared.enums import ProviderType
from app.shared.logger import get_logger

logger = get_logger(__name__)


class ProviderFactory:
    def __init__(self, settings_obj=None):
        self.settings = settings_obj or settings
        self._providers: Dict[ProviderType, BaseAIProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self) -> None:
        """Initializes standard provider adapters."""
        # For Phase 1, we initialize OpenAI adapter
        openai_key = self.settings.openai_api_key or "mock-openai-key-for-local-runs"
        self._providers[ProviderType.OPENAI] = OpenAIProvider(api_key=openai_key)

    def get_provider(self, provider: Union[ProviderType, str]) -> BaseAIProvider:
        """Retrieves or resolves the provider adapter for the requested provider type.

        Args:
            provider: The provider enum type or string identifier.

        Returns:
            An implementation of BaseAIProvider.

        Raises:
            ValueError: If the provider is unsupported or unregistered.
        """
        # Resolve to ProviderType enum if passed as string
        if isinstance(provider, str):
            try:
                provider_type = ProviderType(provider.lower())
            except ValueError:
                logger.error(f"Unknown provider name format: {provider}")
                raise ValueError(f"Unsupported AI Provider: {provider}")
        else:
            provider_type = provider

        resolved_provider = self._providers.get(provider_type)
        if not resolved_provider:
            logger.error(f"AI Provider '{provider_type}' is not registered or initialized.")
            raise ValueError(f"AI Provider '{provider_type}' is not registered.")
            
        return resolved_provider

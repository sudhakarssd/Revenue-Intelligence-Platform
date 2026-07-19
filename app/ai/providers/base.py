from abc import ABC, abstractmethod
from app.ai.contracts import AIRequest, AIResponse


class BaseAIProvider(ABC):
    @abstractmethod
    async def generate(self, request: AIRequest, target_model: str) -> AIResponse:
        """Generate a standardized AIResponse from the AIRequest and target model.

        Args:
            request: The standard platform AIRequest contract.
            target_model: The resolved model name.

        Returns:
            The standard platform AIResponse contract.
        """
        pass

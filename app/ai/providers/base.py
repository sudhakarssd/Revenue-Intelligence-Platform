from abc import ABC, abstractmethod
from app.ai.contracts import AIRequest, AIResponse


class BaseAIProvider(ABC):
    @abstractmethod
    async def generate(self, request: AIRequest) -> AIResponse:
        """Generate a standardized AIResponse from the AIRequest.

        Args:
            request: The standard platform AIRequest contract.

        Returns:
            The standard platform AIResponse contract.
        """
        pass

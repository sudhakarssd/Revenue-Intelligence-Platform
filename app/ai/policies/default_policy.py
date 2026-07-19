from app.ai.contracts import AIRequest
from app.ai.exceptions.exceptions import InvalidRequestException


class DefaultPolicy:
    def evaluate(self, request: AIRequest) -> None:
        """Evaluates global policy rules against the incoming request before routing.

        Args:
            request: The platform AIRequest.

        Raises:
            InvalidRequestException: If the request violates policies (e.g. empty messages).
        """
        if not request.messages:
            raise InvalidRequestException("Policy Violation: AIRequest must contain at least one message.")

        # Ensure message contents are valid and not purely white space
        for idx, message in enumerate(request.messages):
            if not message.content or not message.content.strip():
                raise InvalidRequestException(
                    f"Policy Violation: Message at index {idx} contains empty or missing content."
                )

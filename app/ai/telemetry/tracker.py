import time
from app.ai.contracts import AIRequest, AIResponse
from app.shared.logger import get_logger

logger = get_logger(__name__)


class TelemetryTracker:
    def record_request(self, request: AIRequest) -> float:
        """Starts timing a generation request.

        Returns:
            A start time timestamp float.
        """
        logger.info(f"Telemetry: Initiated request for task '{request.task}'")
        return time.perf_counter()

    def record_response(self, request: AIRequest, response: AIResponse, start_time: float) -> None:
        """Records execution latency and token metrics upon completion."""
        latency = time.perf_counter() - start_time
        total_tokens = response.usage.total_tokens if response.usage else 0
        provider = response.provider_info.provider if response.provider_info else "unknown"
        model = response.provider_info.model if response.provider_info else "unknown"

        logger.info(
            f"Telemetry: Completed task '{request.task}' via provider '{provider}' and model '{model}' "
            f"in {latency:.4f} seconds. Token Usage: {total_tokens} total tokens."
        )

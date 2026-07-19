import pytest
from unittest.mock import AsyncMock, MagicMock
from app.ai.contracts import AIRequest, Message, AIResponse
from app.ai.gateway.gateway import AIGateway
from app.ai.routing.router import ModelRouter
from app.ai.providers.base import BaseAIProvider
from app.ai.providers.factory import ProviderFactory
from app.ai.policies.default_policy import DefaultPolicy
from app.ai.telemetry.tracker import TelemetryTracker
from app.shared.enums import TaskType
from app.ai.exceptions.exceptions import InvalidRequestException


@pytest.mark.asyncio
async def test_gateway_generation_success():
    # Setup mocks
    mock_policy = MagicMock(spec=DefaultPolicy)
    mock_router = MagicMock(spec=ModelRouter)
    mock_router.route.return_value = ("openai", "gpt-4o")

    mock_factory = MagicMock(spec=ProviderFactory)
    mock_provider = MagicMock(spec=BaseAIProvider)
    mock_response = MagicMock(spec=AIResponse)
    mock_provider.generate = AsyncMock(return_value=mock_response)
    mock_factory.get_provider.return_value = mock_provider

    mock_telemetry = MagicMock(spec=TelemetryTracker)
    mock_telemetry.record_request.return_value = 100.0

    # Instantiate gateway with mocks
    gateway = AIGateway(
        policy_engine=mock_policy,
        router=mock_router,
        provider_factory=mock_factory,
        telemetry_tracker=mock_telemetry
    )

    req = AIRequest(task=TaskType.SUMMARIZE, messages=[Message(role="user", content="hello")])
    response = await gateway.generate(req)

    # Assertions on execution sequence
    assert response == mock_response
    mock_policy.evaluate.assert_called_once_with(req)
    mock_router.route.assert_called_once_with(req)
    mock_factory.get_provider.assert_called_once_with("openai")
    mock_telemetry.record_request.assert_called_once_with(req)
    mock_provider.generate.assert_called_once_with(req, target_model="gpt-4o")
    mock_telemetry.record_response.assert_called_once_with(req, mock_response, 100.0)


@pytest.mark.asyncio
async def test_gateway_policy_violation():
    # Use real DefaultPolicy to verify its validation rules
    policy_engine = DefaultPolicy()
    mock_router = MagicMock(spec=ModelRouter)
    mock_factory = MagicMock(spec=ProviderFactory)
    mock_telemetry = MagicMock(spec=TelemetryTracker)

    gateway = AIGateway(
        policy_engine=policy_engine,
        router=mock_router,
        provider_factory=mock_factory,
        telemetry_tracker=mock_telemetry
    )

    # Empty messages violates the DefaultPolicy
    req = AIRequest(task=TaskType.SUMMARIZE, messages=[])

    with pytest.raises(InvalidRequestException) as exc_info:
        await gateway.generate(req)

    assert "AIRequest must contain at least one message" in str(exc_info.value)

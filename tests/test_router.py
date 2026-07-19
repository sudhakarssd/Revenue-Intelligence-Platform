import pytest
from app.ai.contracts import AIRequest, Message
from app.ai.routing.router import ModelRouter
from app.shared.enums import TaskType
from app.ai.exceptions.exceptions import ModelRouteException


def test_router_by_task_enum():
    router = ModelRouter(default_provider="openai", default_model="gpt-4o")
    
    req = AIRequest(
        task=TaskType.SUMMARIZE,
        messages=[Message(role="user", content="hello")]
    )
    provider, target_model = router.route(req)
    
    assert provider == "openai"
    assert target_model == "gpt-4o"


def test_router_by_task_string():
    router = ModelRouter(default_provider="openai", default_model="gpt-4o")
    
    # "analyze" resolves to gpt-4-turbo
    req = AIRequest(
        task="analyze",
        messages=[Message(role="user", content="hello")]
    )
    provider, target_model = router.route(req)
    
    assert provider == "openai"
    assert target_model == "gpt-4-turbo"


def test_router_fallback():
    # Setup router with empty routing table to force fallback
    router = ModelRouter(default_provider="openai", default_model="gpt-4-default", task_routing_table={})
    
    req = AIRequest(
        task=TaskType.CHAT,
        messages=[Message(role="user", content="hello")]
    )
    provider, target_model = router.route(req)
    
    assert provider == "openai"
    assert target_model == "gpt-4-default"


def test_router_unrouteable_error():
    # Disable default routing and routing table
    router = ModelRouter(default_provider="", default_model="", task_routing_table={})
    
    req = AIRequest(
        task=TaskType.CHAT,
        messages=[Message(role="user", content="hello")]
    )
    
    with pytest.raises(ModelRouteException) as exc_info:
        router.route(req)
    
    assert "Unable to route task request" in str(exc_info.value)

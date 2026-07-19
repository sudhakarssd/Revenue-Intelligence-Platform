import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def mock_openai_response():
    """Fixture providing a mock OpenAI API response structure."""
    mock_resp = MagicMock()
    mock_resp.id = "chatcmpl-mock123"
    mock_resp.created = 1718870400
    mock_resp.model = "gpt-4o"
    
    # Setup choice
    mock_choice = MagicMock()
    mock_choice.index = 0
    mock_choice.message.role = "assistant"
    mock_choice.message.content = "Mocked OpenAI completion response."
    mock_choice.finish_reason = "stop"
    mock_resp.choices = [mock_choice]
    
    # Setup usage
    mock_usage = MagicMock()
    mock_usage.prompt_tokens = 15
    mock_usage.completion_tokens = 25
    mock_usage.total_tokens = 40
    mock_resp.usage = mock_usage
    
    return mock_resp


@pytest.fixture
def mock_openai_client(monkeypatch, mock_openai_response):
    """Fixture to mock AsyncOpenAI client responses."""
    mock_client = MagicMock()
    mock_chat = MagicMock()
    mock_completions = MagicMock()
    
    # Make create an async mock returning the mock response
    mock_completions.create = AsyncMock(return_value=mock_openai_response)
    mock_chat.completions = mock_completions
    mock_client.chat = mock_chat
    
    # Patch the AsyncOpenAI constructor in the openai_provider module
    monkeypatch.setattr("app.ai.providers.openai_provider.AsyncOpenAI", MagicMock(return_value=mock_client))
    return mock_client


@pytest.fixture
def client():
    """Fixture providing a FastAPI TestClient."""
    return TestClient(app)

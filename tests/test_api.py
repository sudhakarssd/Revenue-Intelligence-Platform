from fastapi import status


def test_health_check(client):
    """Verifies that the root health check endpoint returns 200 and indicates health."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "default_provider" in data
    assert "default_model" in data


def test_api_ai_generate_success(client, mock_openai_client):
    """Verifies that the /api/v1/ai/generate API successfully maps the request and mock response."""
    payload = {
        "task": "summarize",
        "messages": [
            {"role": "user", "content": "Test content for summarization"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    response = client.post("/api/v1/ai/generate", json=payload)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == "chatcmpl-mock123"
    assert len(data["messages"]) == 1
    assert data["messages"][0]["role"] == "assistant"
    assert data["messages"][0]["content"] == "Mocked OpenAI completion response."
    assert data["usage"]["prompt_tokens"] == 15
    assert data["usage"]["completion_tokens"] == 25
    assert data["usage"]["total_tokens"] == 40
    assert data["provider_info"]["provider"] == "openai"
    assert data["provider_info"]["model"] == "gpt-4o"


def test_api_ai_generate_validation_error(client):
    """Verifies that policy engine violations return HTTP 400 Bad Request."""
    payload = {
        "task": "summarize",
        "messages": []  # Empty messages should trigger default policy exception
    }

    response = client.post("/api/v1/ai/generate", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    data = response.json()
    assert "AIRequest must contain at least one message" in data["detail"]

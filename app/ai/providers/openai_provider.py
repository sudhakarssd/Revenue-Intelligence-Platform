import time
from typing import Optional
from openai import AsyncOpenAI
from app.ai.providers.base import BaseAIProvider
from app.ai.contracts import AIRequest, AIResponse, Message, TokenUsage, ProviderInfo
from app.shared.enums import ProviderType, Role
from app.ai.exceptions.exceptions import ProviderException, RateLimitException


class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def generate(self, request: AIRequest) -> AIResponse:
        # Retrieve resolved target model from extra_params
        target_model = "gpt-4o"
        if request.extra_params and "target_model" in request.extra_params:
            target_model = request.extra_params["target_model"]

        # Construct message dictionaries matching OpenAI format
        messages = [
            {
                "role": msg.role.value if isinstance(msg.role, Role) else str(msg.role),
                "content": msg.content
            }
            for msg in request.messages
        ]
        
        try:
            kwargs = {
                "model": target_model,
                "messages": messages,
            }
            if request.temperature is not None:
                kwargs["temperature"] = request.temperature
            if request.max_tokens is not None:
                kwargs["max_tokens"] = request.max_tokens
            
            if request.extra_params:
                sdk_params = {k: v for k, v in request.extra_params.items() if k != "target_model"}
                kwargs.update(sdk_params)
            
            response = await self.client.chat.completions.create(**kwargs)
            
            # Map choice messages
            output_messages = []
            for choice in response.choices:
                # Safely parse message role to Role enum
                try:
                    role_enum = Role(choice.message.role)
                except ValueError:
                    role_enum = Role.ASSISTANT
                
                output_messages.append(Message(
                    role=role_enum,
                    content=choice.message.content or ""
                ))
            
            # Map token utilization
            usage = None
            if response.usage:
                usage = TokenUsage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens
                )
                
            return AIResponse(
                id=response.id,
                object="ai.response",
                created=response.created,
                messages=output_messages,
                usage=usage,
                provider_info=ProviderInfo(
                    provider=ProviderType.OPENAI,
                    model=response.model
                )
            )
            
        except Exception as e:
            err_msg = str(e)
            cls_name = e.__class__.__name__
            if "RateLimitError" in cls_name or "rate_limit" in err_msg.lower() or "429" in err_msg:
                raise RateLimitException(err_msg, provider="openai")
            else:
                raise ProviderException(err_msg, provider="openai")

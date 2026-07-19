from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.shared.enums import TaskType
from app.ai.contracts.message import Message


class AIRequest(BaseModel):
    task: TaskType = Field(..., description="The high level business task type to execute")
    messages: List[Message] = Field(..., description="Conversation history or prompt messages context")
    temperature: Optional[float] = Field(None, description="Sampling temperature overrides")
    max_tokens: Optional[int] = Field(None, description="Maximum completion tokens limit")
    extra_params: Optional[Dict[str, Any]] = Field(None, description="Optional provider-specific configurations overrides")

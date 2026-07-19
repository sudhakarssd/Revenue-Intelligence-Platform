from pydantic import BaseModel, Field


class TokenUsage(BaseModel):
    prompt_tokens: int = Field(0, description="Number of tokens in the prompt")
    completion_tokens: int = Field(0, description="Number of tokens in the generated completion")
    total_tokens: int = Field(0, description="Total number of tokens used")

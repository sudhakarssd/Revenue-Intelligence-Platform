from pydantic import BaseModel, Field
from app.shared.enums import Role


class Message(BaseModel):
    role: Role = Field(..., description="Role of the message author (system, user, assistant, tool)")
    content: str = Field(..., description="Content of the message")

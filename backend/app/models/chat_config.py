from openai import BaseModel


class ChatConfig(BaseModel):
    domain: str
    title: str = "Chat App"
    system_prompt: str = "You are a helpful assistant."
    password: str | None = None

from openai import BaseModel


class ChatConfig(BaseModel):
    domain: str
    title: str
    bot_aim: str
    password: str
    user: str | None = None
    bot_audience: str | None = None
    bot_tone: str | None = None

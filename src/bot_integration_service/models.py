from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class MessageFromBot(BaseModel):
    """
    Модель для сообщения, полученного от бота
    """
    userid: int = Field(..., description="Идентификатор пользователя на платформе")
    platform: Literal["telegram", "vk"] = Field(..., description="Платформа, откуда пришло сообщение")
    name: str = Field(..., description="Имя пользователя")
    nickname: Optional[str] = Field(None, description="Никнейм пользователя")
    messageid: int = Field(..., description="Идентификатор сообщения")
    message: str = Field(..., description="Текст сообщения")
    date: str = Field(..., description="Дата и время отправки сообщения")


class MessageToBot(BaseModel):
    """
    Модель для сообщения, отправленного на бота
    """
    userid: int = Field(..., description="Идентификатор пользователя на платформе")
    text: str = Field(..., description="Текст сообщения")
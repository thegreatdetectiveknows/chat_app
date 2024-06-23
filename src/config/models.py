from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class MessageFromBot(BaseModel):
    """
    Модель для сообщения, полученного от бота
    """

    userid: int = Field(..., description="Идентификатор пользователя на платформе")
    platform: Literal["telegram", "vk"] = Field(
        ..., description="Платформа, откуда пришло сообщение"
    )
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


class AdminMessage(BaseModel):
    chat_id: str = Field(..., description="ID чата")
    admin_id: str = Field(..., description="ID администратора")
    message_text: str = Field(..., description="Текст сообщения")
    date: str = Field(..., description="Дата отправки сообщения")


class ID_Date(BaseModel):
    id: str = Field(..., description="Идентификатор _id")
    date: str = Field(..., description="Дата и время обновления")


class Message(BaseModel):
    chat_id: str = Field(..., description="_id чата")
    sender_id: str = Field(..., description="_id отправителя")
    message_text: str = Field(..., description="Текст сообщения")
    date: str = Field(..., description="Дата отправки сообщения")


class User(BaseModel):
    user_id: int = Field(..., description="Идентификатор пользователя на платформе")
    platform: str = Field(..., description="Платформа (например, Telegram, VK)")
    name: str = Field(..., description="Имя пользователя")
    nickname: Optional[str] = Field(None, description="Никнейм пользователя")
    registeredAt: str = Field(..., description="Дата регистрации в сервисе")


class Chat(BaseModel):
    user_id: str = Field(..., description="Идентификатор пользователя _id user")
    created_at: str = Field(..., description="Дата создания чата")
    updated_at: str = Field(..., description="Дата последнего обновления чата")

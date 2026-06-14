from typing import Literal

from pydantic import BaseModel, EmailStr, Field


Channel = Literal["email", "telegram", "whatsapp"]
EventType = Literal[
    "onboarding_created",
    "manager_approval_required",
    "missing_documents",
    "document_expiry",
    "workflow_completed",
]


class EmailMessage(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    html_body: str | None = None


class TelegramMessage(BaseModel):
    chat_id: str | None = None
    message: str


class WhatsAppMessage(BaseModel):
    to_phone: str = Field(..., description="E.164 format is preferred, e.g. +971501234567")
    message: str


class NotificationEvent(BaseModel):
    event_type: EventType

    employee_name: str
    employee_email: EmailStr | None = None
    employee_phone: str | None = None

    manager_name: str | None = None
    manager_email: EmailStr | None = None
    manager_phone: str | None = None

    hr_email: EmailStr | None = None
    hr_phone: str | None = None
    telegram_chat_id: str | None = None

    department: str | None = None
    designation: str | None = None
    joining_date: str | None = None

    missing_documents: list[str] = []
    expiry_document: str | None = None
    expiry_date: str | None = None

    channels: list[Channel] = ["email"]


class SendResult(BaseModel):
    channel: Channel
    sent: bool
    preview: bool
    provider_response: dict | None = None
    message: str

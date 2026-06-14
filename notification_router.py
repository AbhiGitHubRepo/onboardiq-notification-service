from fastapi import APIRouter, Depends

from audit import write_audit
from email_smtp import send_email
from schemas import (
    EmailMessage,
    NotificationEvent,
    SendResult,
    TelegramMessage,
    WhatsAppMessage,
)
from security import verify_service_token
from telegram_bot import send_telegram
from templates import build_message
from whatsapp_cloud import send_whatsapp

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/send/email", response_model=SendResult)
def send_email_endpoint(
    message: EmailMessage,
    _: None = Depends(verify_service_token),
) -> SendResult:
    result = send_email(message)
    write_audit(
        "send_email",
        {
            "to": message.to_email,
            "subject": message.subject,
            "result": result.model_dump(),
        },
    )
    return result


@router.post("/send/telegram", response_model=SendResult)
def send_telegram_endpoint(
    message: TelegramMessage,
    _: None = Depends(verify_service_token),
) -> SendResult:
    result = send_telegram(message)
    write_audit(
        "send_telegram",
        {
            "chat_id": message.chat_id,
            "result": result.model_dump(),
        },
    )
    return result


@router.post("/send/whatsapp", response_model=SendResult)
def send_whatsapp_endpoint(
    message: WhatsAppMessage,
    _: None = Depends(verify_service_token),
) -> SendResult:
    result = send_whatsapp(message)
    write_audit(
        "send_whatsapp",
        {
            "to": message.to_phone,
            "result": result.model_dump(),
        },
    )
    return result


@router.post("/event", response_model=list[SendResult])
def send_event_notification(
    event: NotificationEvent,
    _: None = Depends(verify_service_token),
) -> list[SendResult]:
    subject, body = build_message(event)
    results: list[SendResult] = []

    if "email" in event.channels:
        to_email = event.employee_email or event.manager_email or event.hr_email
        if to_email:
            results.append(
                send_email(
                    EmailMessage(
                        to_email=to_email,
                        subject=subject,
                        body=body,
                    )
                )
            )
        else:
            results.append(
                SendResult(
                    channel="email",
                    sent=False,
                    preview=False,
                    provider_response={"error": "No email recipient supplied"},
                    message="No email recipient supplied.",
                )
            )

    if "telegram" in event.channels:
        results.append(
            send_telegram(
                TelegramMessage(
                    chat_id=event.telegram_chat_id,
                    message=f"{subject}\n\n{body}",
                )
            )
        )

    if "whatsapp" in event.channels:
        to_phone = event.employee_phone or event.manager_phone or event.hr_phone
        if to_phone:
            results.append(
                send_whatsapp(
                    WhatsAppMessage(
                        to_phone=to_phone,
                        message=f"{subject}\n\n{body}",
                    )
                )
            )
        else:
            results.append(
                SendResult(
                    channel="whatsapp",
                    sent=False,
                    preview=False,
                    provider_response={"error": "No WhatsApp recipient supplied"},
                    message="No WhatsApp recipient supplied.",
                )
            )

    write_audit(
        "event_notification",
        {
            "event_type": event.event_type,
            "employee": event.employee_name,
            "channels": event.channels,
            "results": [r.model_dump() for r in results],
        },
    )
    return results

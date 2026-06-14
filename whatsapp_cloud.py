import re

import requests

from config import settings
from schemas import SendResult, WhatsAppMessage


def normalize_phone(phone: str) -> str:
    cleaned = re.sub(r"[^\d+]", "", phone or "")
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    if cleaned.startswith("00"):
        cleaned = cleaned[2:]
    if cleaned and len(cleaned) <= 10 and not cleaned.startswith(settings.whatsapp_default_country_code):
        cleaned = settings.whatsapp_default_country_code + cleaned
    return cleaned


def send_whatsapp(message: WhatsAppMessage) -> SendResult:
    phone = normalize_phone(message.to_phone)

    if settings.preview_mode:
        return SendResult(
            channel="whatsapp",
            sent=False,
            preview=True,
            provider_response=None,
            message=f"Preview WhatsApp to {phone}: {message.message[:120]}",
        )

    if not settings.whatsapp_access_token or not settings.whatsapp_phone_number_id:
        return SendResult(
            channel="whatsapp",
            sent=False,
            preview=False,
            provider_response={"error": "WhatsApp Cloud API not configured"},
            message="WhatsApp Cloud API settings are missing.",
        )

    url = (
        f"https://graph.facebook.com/{settings.whatsapp_api_version}/"
        f"{settings.whatsapp_phone_number_id}/messages"
    )

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message.message,
        },
    }

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=20)

    try:
        provider_json = response.json()
    except Exception:
        provider_json = {"text": response.text}

    ok = 200 <= response.status_code < 300

    return SendResult(
        channel="whatsapp",
        sent=ok,
        preview=False,
        provider_response=provider_json,
        message="WhatsApp message sent." if ok else "WhatsApp send failed.",
    )

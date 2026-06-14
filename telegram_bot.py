import requests

from config import settings
from schemas import SendResult, TelegramMessage


def send_telegram(message: TelegramMessage) -> SendResult:
    """
    Safe Telegram sender.

    Important:
    Hugging Face Spaces can sometimes timeout while calling api.telegram.org.
    This function catches those network errors and returns a clean SendResult
    instead of crashing FastAPI with 500 Internal Server Error.
    """
    chat_id = message.chat_id or settings.telegram_default_chat_id

    if settings.preview_mode:
        return SendResult(
            channel="telegram",
            sent=False,
            preview=True,
            provider_response={
                "chat_id_configured": bool(chat_id),
                "bot_token_configured": bool(settings.telegram_bot_token),
            },
            message=f"Preview Telegram to {chat_id or 'not configured'}: {message.message[:120]}",
        )

    if not settings.telegram_bot_token or not chat_id:
        return SendResult(
            channel="telegram",
            sent=False,
            preview=False,
            provider_response={
                "error": "Telegram bot token or chat ID missing",
                "bot_token_configured": bool(settings.telegram_bot_token),
                "chat_id_configured": bool(chat_id),
            },
            message="Telegram settings are missing.",
        )

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": str(chat_id),
        "text": message.message,
        "disable_web_page_preview": True,
    }

    try:
        # Shorter timeout avoids long hanging requests on Hugging Face.
        response = requests.post(url, json=payload, timeout=8)

        try:
            provider_json = response.json()
        except Exception:
            provider_json = {"text": response.text[:1000]}

        ok = 200 <= response.status_code < 300 and provider_json.get("ok", False)

        return SendResult(
            channel="telegram",
            sent=ok,
            preview=False,
            provider_response=provider_json,
            message="Telegram message sent." if ok else "Telegram send failed.",
        )

    except requests.exceptions.Timeout as exc:
        return SendResult(
            channel="telegram",
            sent=False,
            preview=False,
            provider_response={
                "error": "Telegram API timeout",
                "detail": str(exc),
                "host": "api.telegram.org",
                "recommendation": "Hugging Face Space could not reach Telegram in time. Try again later or host the notification service on Render/Railway for reliable outbound calls.",
            },
            message="Telegram API timed out. Notification-service did not crash.",
        )

    except requests.exceptions.RequestException as exc:
        return SendResult(
            channel="telegram",
            sent=False,
            preview=False,
            provider_response={
                "error": "Telegram API request failed",
                "detail": str(exc),
                "host": "api.telegram.org",
            },
            message="Telegram API request failed. Notification-service did not crash.",
        )

    except Exception as exc:
        return SendResult(
            channel="telegram",
            sent=False,
            preview=False,
            provider_response={
                "error": "Unexpected Telegram sender error",
                "detail": str(exc),
            },
            message="Telegram sender failed safely. Notification-service did not crash.",
        )

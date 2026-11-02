from fastapi import FastAPI

from config import settings
from notification_router import router as notification_router
from desi_bawarchi_router import router as desi_bawarchi_router


app = FastAPI(
    title="OnboardIQ Notification Service",
    description="Root-file service for Email, Telegram and WhatsApp notifications.",
    version="1.0.0",
)

app.include_router(notification_router)
app.include_router(desi_bawarchi_router)


@app.get("/")
def root():
    return {
        "service": "OnboardIQ Notification Service",
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "preview_mode": settings.preview_mode,
        "smtp_configured": bool(settings.smtp_host and settings.smtp_username and settings.smtp_password),
        "telegram_configured": bool(settings.telegram_bot_token and settings.telegram_default_chat_id),
        "whatsapp_configured": bool(settings.whatsapp_access_token and settings.whatsapp_phone_number_id),
    }

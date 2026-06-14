from fastapi import Header, HTTPException, status

from config import settings


def verify_service_token(x_notification_token: str | None = Header(default=None)) -> None:
    if not x_notification_token or x_notification_token != settings.notification_api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Notification-Token",
        )

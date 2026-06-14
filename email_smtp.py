import smtplib
from email.message import EmailMessage as MimeEmailMessage

from config import settings
from schemas import EmailMessage, SendResult


def send_email(message: EmailMessage) -> SendResult:
    if settings.preview_mode:
        return SendResult(
            channel="email",
            sent=False,
            preview=True,
            provider_response=None,
            message=f"Preview email to {message.to_email}: {message.subject}",
        )

    if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password:
        return SendResult(
            channel="email",
            sent=False,
            preview=False,
            provider_response={"error": "SMTP not configured"},
            message="SMTP settings are missing.",
        )

    msg = MimeEmailMessage()
    msg["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    msg["To"] = message.to_email
    msg["Subject"] = message.subject
    msg.set_content(message.body)

    if message.html_body:
        msg.add_alternative(message.html_body, subtype="html")

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg)

    return SendResult(
        channel="email",
        sent=True,
        preview=False,
        provider_response={"status": "sent"},
        message=f"Email sent to {message.to_email}",
    )

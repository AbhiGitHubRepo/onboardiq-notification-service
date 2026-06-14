---
title: OnboardIQ Notification Service
emoji: 🔔
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# OnboardIQ Notification Service

Hugging Face friendly version with **root files only** and **no folder structure**.

Upload all files directly into the Space root.

## Files

```text
README.md
Dockerfile
requirements.txt
app.py
config.py
schemas.py
security.py
audit.py
templates.py
email_smtp.py
telegram_bot.py
whatsapp_cloud.py
notification_router.py
```

## Required secrets

```text
NOTIFICATION_API_TOKEN=your-secret-token
PREVIEW_MODE=true
```

## Optional Email SMTP secrets

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=OnboardIQ HR
```

## Optional Telegram secrets

```text
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_DEFAULT_CHAT_ID=your-chat-id
```

## Optional WhatsApp secrets

```text
WHATSAPP_ACCESS_TOKEN=your-whatsapp-cloud-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_API_VERSION=v20.0
WHATSAPP_DEFAULT_COUNTRY_CODE=971
```

## Test after deployment

```text
/health
/docs
```

"""Additive Desi Bawarchi Telegram route for the existing OnboardIQ Render notification service.

Copy this file beside the existing notification-service config.py, then include its router
from the existing FastAPI main file. It does not modify /notifications/event.
"""
import os, secrets, requests
from typing import Optional
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

try:
    from config import settings
except Exception:
    settings = None

router = APIRouter()

class DesiBawarchiNotification(BaseModel):
    event_type: str = Field(max_length=80)
    entity_id: str = Field(max_length=120)
    message: str = Field(min_length=1, max_length=4000)
    lead_type: str = Field(default='', max_length=80)
    lead_id: str = Field(default='', max_length=120)
    customer_name: str = Field(default='', max_length=160)
    customer_phone: str = Field(default='', max_length=80)
    customer_email: str = Field(default='', max_length=200)
    telegram_chat_id: Optional[str] = Field(default=None, max_length=120)


def _setting(name: str, env: str = ''):
    if settings is not None and hasattr(settings, name):
        return getattr(settings, name)
    return os.getenv(env or name.upper(), '')


def _check_token(value: Optional[str]):
    expected = str(_setting('notification_api_token', 'NOTIFICATION_API_TOKEN') or '')
    supplied = str(value or '')
    if not expected:
        raise HTTPException(status_code=503, detail='Notification API token is not configured')
    if not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail='Invalid notification token')


@router.post('/notifications/desi-bawarchi')
def desi_bawarchi_notification(payload: DesiBawarchiNotification, x_notification_token: Optional[str] = Header(None)):
    _check_token(x_notification_token)
    bot_token = str(_setting('telegram_bot_token', 'TELEGRAM_BOT_TOKEN') or '')
    default_chat = str(_setting('telegram_default_chat_id', 'TELEGRAM_DEFAULT_CHAT_ID') or '')
    chat_id = str(payload.telegram_chat_id or default_chat or '')
    preview = bool(_setting('preview_mode', 'PREVIEW_MODE'))

    if preview:
        return {'channel':'telegram','sent':False,'preview':True,'message':'Preview mode: Desi Bawarchi notification accepted.'}
    if not bot_token or not chat_id:
        raise HTTPException(status_code=503, detail='Telegram bot token or default chat ID is not configured')

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    try:
        r = requests.post(url, json={'chat_id':chat_id,'text':payload.message,'disable_web_page_preview':True}, timeout=8)
        try:
            body = r.json()
        except Exception:
            body = {'raw': r.text[:600]}
        if not (200 <= r.status_code < 300 and body.get('ok', False)):
            raise HTTPException(status_code=502, detail='Telegram provider rejected the notification')
        return {'channel':'telegram','sent':True,'preview':False,'event_type':payload.event_type,'entity_id':payload.entity_id}
    except HTTPException:
        raise
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail='Telegram provider timeout')
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail='Telegram provider request failed')

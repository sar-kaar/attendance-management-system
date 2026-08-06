"""Push-notification send service (B6).

Provider-gated so the mobile team can develop against it before real push
credentials exist, mirroring the FACE_PROVIDER pattern already in this codebase.

    PUSH_PROVIDER = 'console'  (default) — logs, sends nothing. Safe for dev/CI.
    PUSH_PROVIDER = 'expo'              — POSTs to Expo's push API.

`send_to_user(user, title, body, data=None)` fans out to that user's active
devices and returns the number of devices a message was dispatched to.
"""
import logging

import requests
from django.conf import settings

from .models import Device

logger = logging.getLogger(__name__)

EXPO_PUSH_URL = 'https://exp.host/--/api/v2/push/send'


def _provider():
    return getattr(settings, 'PUSH_PROVIDER', 'console')


def send_to_user(user, title, body, data=None):
    """Send a push to all of `user`'s active devices. Returns count dispatched."""
    tokens = list(
        Device.objects.filter(user=user, is_active=True).values_list('token', flat=True)
    )
    if not tokens:
        return 0
    return send_to_tokens(tokens, title, body, data)


def send_to_tokens(tokens, title, body, data=None):
    provider = _provider()
    if provider == 'expo':
        return _send_expo(tokens, title, body, data)
    # 'console' / unknown → log only, never raise.
    logger.info('[push:console] to=%s title=%r body=%r data=%r', tokens, title, body, data)
    return len(tokens)


def _send_expo(tokens, title, body, data):
    messages = [
        {'to': t, 'title': title, 'body': body, 'data': data or {}}
        for t in tokens
    ]
    try:
        resp = requests.post(EXPO_PUSH_URL, json=messages, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        logger.exception('[push:expo] send failed for %d token(s)', len(tokens))
        return 0
    return len(tokens)

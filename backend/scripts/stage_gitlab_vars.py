"""Collect deployment credentials from local source files into one paste-ready
staging file for GitLab CI/CD Variables.

Values are read and written locally only - nothing is printed to stdout, so the
secrets never land in a terminal scrollback or an agent transcript. The output
file lives outside the repo and should be deleted once the variables are in
GitLab.

Usage:
    python backend/scripts/stage_gitlab_vars.py
"""

import json
import re
from pathlib import Path

SOURCE_DIR = Path(r'D:\CSE Project')
OUT_PATH = SOURCE_DIR / 'gitlab-variables-PASTE-THEN-DELETE.txt'

GOOGLE_JSON = next(SOURCE_DIR.glob('client_secret_*.apps.googleusercontent.com.json'), None)
FACEBOOK_JS = SOURCE_DIR / 'facebookOauth.js'
BREVO_TXT = SOURCE_DIR / 'brevo.txt'

# Not secret, but they belong with the set so everything is pasted in one pass.
STATIC = {
    'EMAIL_HOST': 'smtp-relay.brevo.com',
    'EMAIL_PORT': '587',
    'EMAIL_USE_TLS': 'True',
    'DEFAULT_FROM_EMAIL': 'AMS <rokayaabi123@gmail.com>',
    'OTP_EXPIRY_MINUTES': '10',
}

# Which variables must be flagged Masked in GitLab. Masking hides the value in
# job logs; GitLab rejects values containing '@' or shorter than 8 chars, which
# is why the SMTP *login* is not in this set even though it is a credential.
MASK = {'EMAIL_HOST_PASSWORD', 'GOOGLE_CLIENT_SECRET', 'FACEBOOK_APP_SECRET'}


def read(path):
    return path.read_text(encoding='utf-8', errors='ignore') if path and path.exists() else ''


def collect():
    values = dict(STATIC)
    missing = []

    brevo = read(BREVO_TXT)
    smtp_key = re.search(r'xsmtpsib-[A-Za-z0-9-]+', brevo)
    login = re.search(r'[A-Za-z0-9._%+-]+@smtp-brevo\.com', brevo)
    values['EMAIL_HOST_PASSWORD'] = smtp_key.group(0) if smtp_key else missing.append('EMAIL_HOST_PASSWORD')
    values['EMAIL_HOST_USER'] = login.group(0) if login else missing.append('EMAIL_HOST_USER')

    if GOOGLE_JSON and GOOGLE_JSON.exists():
        web = json.loads(read(GOOGLE_JSON)).get('web', {})
        values['GOOGLE_CLIENT_ID'] = web.get('client_id', '')
        values['GOOGLE_CLIENT_SECRET'] = web.get('client_secret', '')
    else:
        missing += ['GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET']

    fb = read(FACEBOOK_JS)
    # The file mixes real values with Facebook's own SDK boilerplate, so match
    # the concrete formats: numeric app id, 32-char hex secret.
    app_id = re.search(r'\b\d{15,17}\b', fb)
    app_secret = re.search(r'\b[a-f0-9]{32}\b', fb)
    values['FACEBOOK_APP_ID'] = app_id.group(0) if app_id else missing.append('FACEBOOK_APP_ID')
    values['FACEBOOK_APP_SECRET'] = app_secret.group(0) if app_secret else missing.append('FACEBOOK_APP_SECRET')

    return {k: v for k, v in values.items() if v}, [m for m in missing if m]


def main():
    values, missing = collect()

    order = [
        'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS', 'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL', 'OTP_EXPIRY_MINUTES',
        'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET',
        'FACEBOOK_APP_ID', 'FACEBOOK_APP_SECRET',
    ]

    lines = [
        'GitLab CI/CD Variables - paste each into',
        'GitLab > Settings > CI/CD > Variables > Add variable',
        '',
        'For every one: Protected = YES.',
        'Mask only the three marked [MASK] - GitLab rejects masking values',
        'that contain "@" or are under 8 characters.',
        '',
        'DELETE THIS FILE once the variables are saved in GitLab.',
        '=' * 60,
        '',
    ]
    for name in order:
        if name in values:
            tag = '  [MASK]' if name in MASK else ''
            lines.append(f'{name}{tag}')
            lines.append(values[name])
            lines.append('')

    if missing:
        lines += ['', 'COULD NOT FIND IN SOURCE FILES:'] + [f'  - {m}' for m in missing]

    OUT_PATH.write_text('\n'.join(lines), encoding='utf-8')
    # Deliberately reports only counts and names - never a value.
    print(f'Wrote {len(values)} variables to:')
    print(f'  {OUT_PATH}')
    if missing:
        print(f'Missing {len(missing)}: {", ".join(missing)}')


if __name__ == '__main__':
    main()

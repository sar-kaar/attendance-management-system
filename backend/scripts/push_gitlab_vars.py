"""Push deployment credentials from local source files into GitLab CI/CD variables.

Reads the values locally and sends them straight to the GitLab API, so the
secrets never pass through a terminal, a chat transcript, or the repo. Only key
names and HTTP outcomes are printed.

Auth: set a GitLab personal access token with the `api` scope in the
GITLAB_TOKEN environment variable. Create one at
https://gitlab.com/-/user_settings/personal_access_tokens

Usage (PowerShell):
    $env:GITLAB_TOKEN = "<your-token>"
    .venv-win\\Scripts\\python.exe backend\\scripts\\push_gitlab_vars.py --dry-run
    .venv-win\\Scripts\\python.exe backend\\scripts\\push_gitlab_vars.py

--dry-run reports what would change without sending any value.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE_DIR = Path(r'D:\CSE Project')
PROJECT_PATH = 'rokayaabi123/attendance-management-system'
API_ROOT = 'https://gitlab.com/api/v4'

GOOGLE_JSON = next(SOURCE_DIR.glob('client_secret_*.apps.googleusercontent.com.json'), None)
FACEBOOK_JS = SOURCE_DIR / 'facebookOauth.js'
BREVO_TXT = SOURCE_DIR / 'brevo.txt'

STATIC = {
    'EMAIL_HOST': 'smtp-relay.brevo.com',
    'EMAIL_PORT': '587',
    'EMAIL_USE_TLS': 'True',
    'DEFAULT_FROM_EMAIL': 'AMS <rokayaabi123@gmail.com>',
    'OTP_EXPIRY_MINUTES': '10',
}

# GitLab rejects masking for values containing '@', spaces, or '<' '>', which
# rules out the login and From address even though they are credentials.
MASK = {'EMAIL_HOST_PASSWORD', 'GOOGLE_CLIENT_SECRET', 'FACEBOOK_APP_SECRET',
        'BREVO_API_KEY'}

ORDER = [
    'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS', 'EMAIL_HOST_USER',
    'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL', 'OTP_EXPIRY_MINUTES',
    'BREVO_API_KEY',
    'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET',
    'FACEBOOK_APP_ID', 'FACEBOOK_APP_SECRET',
]


def read(path):
    return path.read_text(encoding='utf-8', errors='ignore') if path and path.exists() else ''


def collect():
    """Pull every credential out of the local source files."""
    values = dict(STATIC)
    missing = []

    brevo = read(BREVO_TXT)
    smtp_key = re.search(r'xsmtpsib-[A-Za-z0-9-]+', brevo)
    login = re.search(r'[A-Za-z0-9._%+-]+@smtp-brevo\.com', brevo)
    if smtp_key:
        values['EMAIL_HOST_PASSWORD'] = smtp_key.group(0)
    else:
        missing.append('EMAIL_HOST_PASSWORD')
    if login:
        values['EMAIL_HOST_USER'] = login.group(0)
    else:
        missing.append('EMAIL_HOST_USER')

    # Brevo's v3 HTTP API key - separate credential from the SMTP key above,
    # needed for anything that talks to api.brevo.com rather than the relay.
    api_key = re.search(r'xkeysib-[A-Za-z0-9-]+', brevo)
    if api_key:
        values['BREVO_API_KEY'] = api_key.group(0)
    else:
        missing.append('BREVO_API_KEY')

    if GOOGLE_JSON and GOOGLE_JSON.exists():
        web = json.loads(read(GOOGLE_JSON)).get('web', {})
        for name, field in (('GOOGLE_CLIENT_ID', 'client_id'),
                            ('GOOGLE_CLIENT_SECRET', 'client_secret')):
            if web.get(field):
                values[name] = web[field]
            else:
                missing.append(name)
    else:
        missing += ['GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET']

    fb = read(FACEBOOK_JS)
    # The file mixes real values with Facebook's SDK boilerplate, so match the
    # concrete formats rather than variable names: numeric app id, hex secret.
    app_id = re.search(r'\b\d{15,17}\b', fb)
    app_secret = re.search(r'\b[a-f0-9]{32}\b', fb)
    if app_id:
        values['FACEBOOK_APP_ID'] = app_id.group(0)
    else:
        missing.append('FACEBOOK_APP_ID')
    if app_secret:
        values['FACEBOOK_APP_SECRET'] = app_secret.group(0)
    else:
        missing.append('FACEBOOK_APP_SECRET')

    return values, missing


def api(token, method, path, payload=None):
    url = f'{API_ROOT}{path}'
    data = urllib.parse.urlencode(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('PRIVATE-TOKEN', token)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode() or '{}')
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')
        try:
            return e.code, json.loads(body or '{}')
        except ValueError:
            return e.code, {'raw': body[:200]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true',
                        help='report planned changes without sending values')
    args = parser.parse_args()

    token = os.environ.get('GITLAB_TOKEN', '').strip()
    if not token:
        # Fall back to the local token file. Read here rather than passed on the
        # command line so the token never lands in shell history.
        token_file = SOURCE_DIR / 'gitlab.api'
        if token_file.exists():
            # Match to end-of-line, not a character class: newer GitLab tokens
            # are routable and contain '.' separators, which a narrow class
            # silently truncates into a valid-looking but wrong token.
            found = re.search(r'^\s*(glpat-\S+)\s*$', token_file.read_text(
                encoding='utf-8', errors='ignore'), re.M)
            if found:
                token = found.group(1)
                print(f'Using token from {token_file.name}')
    if not token and not args.dry_run:
        sys.exit('No token. Set GITLAB_TOKEN or put a glpat- token in '
                 f'{SOURCE_DIR / "gitlab.api"}')

    values, missing = collect()
    if missing:
        print('WARNING - not found in source files:', ', '.join(missing))

    project = urllib.parse.quote(PROJECT_PATH, safe='')

    existing = set()
    if token:
        status, body = api(token, 'GET', f'/projects/{project}/variables?per_page=100')
        if status != 200:
            sys.exit(f'Could not list variables (HTTP {status}): {str(body)[:200]}')
        existing = {v['key'] for v in body}
        print(f'Existing variables in project: {len(existing)}')

    planned = [k for k in ORDER if k in values]
    print(f'Variables to push: {len(planned)}')

    if args.dry_run:
        for key in planned:
            action = 'UPDATE' if key in existing else 'CREATE'
            print(f'  {action:6} {key}{"  [masked]" if key in MASK else ""}')
        print('\nDry run - nothing was sent.')
        return

    ok = failed = 0
    for key in planned:
        payload = {
            'key': key,
            'value': values[key],
            'protected': 'true',
            'masked': 'true' if key in MASK else 'false',
            'environment_scope': '*',
        }
        if key in existing:
            payload.pop('key')
            status, body = api(token, 'PUT', f'/projects/{project}/variables/{key}', payload)
        else:
            status, body = api(token, 'POST', f'/projects/{project}/variables', payload)

        if status in (200, 201):
            print(f'  OK      {key}')
            ok += 1
        else:
            # Never echo the value - only GitLab's complaint about it.
            print(f'  FAILED  {key} (HTTP {status}): {str(body)[:160]}')
            failed += 1

    print(f'\nDone. {ok} succeeded, {failed} failed.')
    if failed:
        print('Masking errors usually mean the value has characters GitLab '
              'cannot mask; rerun after removing that key from MASK.')


if __name__ == '__main__':
    main()

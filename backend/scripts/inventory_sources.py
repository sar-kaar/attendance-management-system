"""Report every credential-ish field present in the local source files.

Prints field names, formats, and lengths only - never a value - so the full
contents can be audited without leaking anything into a terminal or transcript.
"""

import json
import re
from pathlib import Path

SOURCE_DIR = Path(r'D:\CSE Project')

PATTERNS = [
    ('Brevo SMTP key', r'xsmtpsib-[A-Za-z0-9-]+'),
    ('Brevo API key (v3)', r'xkeysib-[A-Za-z0-9-]+'),
    ('Google client secret', r'GOCSPX-[A-Za-z0-9_-]+'),
    ('Google client id', r'\d+-[a-z0-9]+\.apps\.googleusercontent\.com'),
    ('32-char hex (fb app secret)', r'\b[a-f0-9]{32}\b'),
    ('Long numeric id (fb app id)', r'\b\d{15,17}\b'),
    ('Email address', r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
    ('Bearer/JWT-ish', r'\bey[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'),
    ('AWS-style key', r'\bAKIA[0-9A-Z]{16}\b'),
    ('Generic long token', r'\b[A-Za-z0-9_-]{40,}\b'),
]


def scan(path):
    print(f'\n{"=" * 70}\nFILE: {path.name}  ({path.stat().st_size} bytes)')
    text = path.read_text(encoding='utf-8', errors='ignore')
    lines = [l for l in text.splitlines() if l.strip()]
    print(f'non-empty lines: {len(lines)}')

    if path.suffix == '.json':
        try:
            data = json.loads(text)
            print('JSON structure:')
            for top, inner in data.items():
                print(f'  "{top}":')
                if isinstance(inner, dict):
                    for k, v in inner.items():
                        if isinstance(v, list):
                            print(f'     {k}: list[{len(v)}]')
                            for item in v:
                                print(f'        - {item}')
                        else:
                            print(f'     {k}: <{len(str(v))} chars>')
        except ValueError as e:
            print('  invalid JSON:', e)

    print('credential patterns found:')
    any_found = False
    for label, pat in PATTERNS:
        hits = re.findall(pat, text)
        uniq = sorted(set(hits))
        if uniq:
            any_found = True
            for h in uniq:
                # Emails and public identifiers are safe to show in full;
                # anything secret-shaped is reported by length only.
                safe = label in ('Email address', 'Google client id',
                                 'Long numeric id (fb app id)')
                shown = h if safe else f'<{len(h)} chars, starts "{h[:9]}...">'
                print(f'  [{label}] {shown}')
    if not any_found:
        print('  (none)')

    # Surface any KEY=VALUE / "key": style field names not covered above.
    names = set(re.findall(r'^\s*([A-Za-z_][A-Za-z0-9_]{2,})\s*[:=]', text, re.M))
    if names:
        print('field names present:', ', '.join(sorted(names)[:25]))


def main():
    targets = sorted(SOURCE_DIR.glob('client_secret_*.json'))
    targets += [SOURCE_DIR / 'facebookOauth.js', SOURCE_DIR / 'brevo.txt']
    for p in targets:
        if p.exists():
            scan(p)
        else:
            print(f'\nMISSING: {p}')


if __name__ == '__main__':
    main()

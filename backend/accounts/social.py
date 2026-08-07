"""Server-side verification of Google and Facebook sign-in credentials.

The browser is only ever trusted to *carry* a credential, never to assert who
the user is: it obtains a token from the provider and posts it here, and this
module validates that token directly against the provider before any account is
created or any of our JWTs are issued. A forged or replayed token fails here.

Nothing in this module is reachable from the client - the Google client secret
and Facebook app secret stay on the server.
"""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

logger = logging.getLogger(__name__)

User = get_user_model()

GOOGLE_ISSUERS = ('accounts.google.com', 'https://accounts.google.com')
FACEBOOK_GRAPH = 'https://graph.facebook.com/v21.0'


class SocialAuthError(Exception):
    """Raised when a provider credential can't be validated."""


@transaction.atomic
def get_social_user(email, first_name='', last_name=''):
    """Find the account for a verified provider email.

    Matching is by email because that is the only identifier both providers
    agree on. Social sign-in never creates an account: without this check,
    anyone with a Gmail/Facebook account could sign in and be silently
    provisioned a new account, regardless of whether they were ever meant
    to have access. Accounts must be created by an administrator (or via
    direct registration) first; social sign-in only links to one that
    already exists.
    """
    email = (email or '').strip().lower()
    if not email:
        raise SocialAuthError('The provider did not return an email address.')

    user = User.objects.filter(email__iexact=email).first()
    if not user:
        raise SocialAuthError(
            'No account exists for this email address. Contact your '
            'administrator to have an account created before signing in.'
        )
    return user


def verify_google_token(id_token_str):
    """Validate a Google ID token and return its verified claims.

    google-auth checks the RS256 signature against Google's rotating public
    keys, the expiry, and that the audience is our client id - the audience
    check is what stops a token minted for some other application from being
    replayed against us.
    """
    if not id_token_str:
        raise SocialAuthError('No Google credential was supplied.')

    client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    if not client_id:
        raise SocialAuthError('Google sign-in is not configured on the server.')

    try:
        from google.auth.transport import requests as google_requests
        from google.oauth2 import id_token as google_id_token
    except ImportError:
        logger.exception('google-auth is not installed')
        raise SocialAuthError('Google sign-in is unavailable on the server.')

    try:
        claims = google_id_token.verify_oauth2_token(
            id_token_str, google_requests.Request(), client_id
        )
    except ValueError as exc:
        logger.warning('Rejected Google credential: %s', exc)
        raise SocialAuthError('Google sign-in failed verification.')

    if claims.get('iss') not in GOOGLE_ISSUERS:
        raise SocialAuthError('Google sign-in failed verification.')

    # An unverified email would let someone register a Google account against
    # an address they do not control and inherit any account we match by email.
    if not claims.get('email_verified'):
        raise SocialAuthError('This Google account has an unverified email address.')

    return {
        'email': claims.get('email'),
        'first_name': claims.get('given_name', ''),
        'last_name': claims.get('family_name', ''),
    }


def verify_facebook_token(access_token):
    """Validate a Facebook user access token and return the user's details.

    debug_token is the step that matters: it confirms the token was issued for
    *our* app and is still valid. Skipping it and simply calling /me would
    happily accept a token minted for any other Facebook app.
    """
    if not access_token:
        raise SocialAuthError('No Facebook credential was supplied.')

    app_id = getattr(settings, 'FACEBOOK_APP_ID', '')
    app_secret = getattr(settings, 'FACEBOOK_APP_SECRET', '')
    if not app_id or not app_secret:
        raise SocialAuthError('Facebook sign-in is not configured on the server.')

    try:
        import requests
    except ImportError:
        logger.exception('requests is not installed')
        raise SocialAuthError('Facebook sign-in is unavailable on the server.')

    try:
        debug = requests.get(
            f'{FACEBOOK_GRAPH}/debug_token',
            params={'input_token': access_token,
                    'access_token': f'{app_id}|{app_secret}'},
            timeout=15,
        ).json().get('data', {})
    except requests.RequestException:
        logger.exception('Could not reach Facebook to verify a token')
        raise SocialAuthError('Could not reach Facebook. Please try again.')

    if not debug.get('is_valid'):
        raise SocialAuthError('Facebook sign-in failed verification.')
    if str(debug.get('app_id')) != str(app_id):
        logger.warning('Facebook token was issued for app %s, not ours', debug.get('app_id'))
        raise SocialAuthError('Facebook sign-in failed verification.')

    try:
        profile = requests.get(
            f'{FACEBOOK_GRAPH}/me',
            params={'fields': 'email,first_name,last_name', 'access_token': access_token},
            timeout=15,
        ).json()
    except requests.RequestException:
        logger.exception('Could not fetch the Facebook profile')
        raise SocialAuthError('Could not reach Facebook. Please try again.')

    if not profile.get('email'):
        # Facebook omits email when the user hides it or the account has none.
        raise SocialAuthError(
            'Your Facebook account did not share an email address, which we need '
            'to create your account. Please sign in with Google or register directly.'
        )

    return {
        'email': profile['email'],
        'first_name': profile.get('first_name', ''),
        'last_name': profile.get('last_name', ''),
    }

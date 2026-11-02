import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone


def generate_secure_token(length=32):
    return secrets.token_urlsafe(length)


def hash_token(token):
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def verify_token(token, token_hash):
    if not token or not token_hash:
        return False

    return hmac.compare_digest(
        hash_token(token),
        token_hash
    )


def generate_password_reset_token():
    token = generate_secure_token(48)
    return token, hash_token(token)


def generate_email_verification_token():
    token = generate_secure_token(48)
    return token, hash_token(token)


def token_expiry(hours=1):
    return datetime.now(
        timezone.utc
    ) + timedelta(hours=hours)


def password_reset_expiry(hours=1):
    return token_expiry(hours)


def email_verification_expiry(hours=24):
    return token_expiry(hours)


def is_token_expired(expires_at):
    if not expires_at:
        return True

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    return datetime.now(
        timezone.utc
    ) >= expires_at


def constant_time_compare(value_a, value_b):
    if value_a is None or value_b is None:
        return False

    return hmac.compare_digest(
        str(value_a),
        str(value_b)
    )


def secure_random_filename(extension):
    extension = str(
        extension or ""
    ).strip().lstrip(".").lower()

    filename = secrets.token_hex(32)

    if extension:
        return f"{filename}.{extension}"

    return filename
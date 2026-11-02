from ..extensions import db
from ..models import User
from ..utils.security import (generate_password_reset_token,hash_token,is_token_expired,password_reset_expiry,)

def authenticate_user(email, password):
    user = User.from_row(db.fetchone("SELECT * FROM users WHERE email=%s LIMIT 1",(email.strip().lower(),)))
    if not user or not user.is_active:
        return None
    if not user.check_password(password):
        return None
    return user

def create_user(name, email, password, role="staff"):
    name = name.strip()
    email = email.strip().lower()

    user = User(name=name,email=email,role=role)
    user.set_password(password)
    user.id = db.execute("""
        INSERT INTO users
        (name, email, password_hash, role, is_active, email_verified)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            user.name,
            user.email,
            user.password_hash,
            user.role,
            1,
            0
        )
    )

    user.is_active = 1
    user.email_verified = 0

    return user

def update_password(user, password):
    user.set_password(password)
    db.execute("UPDATE users SET password_hash=%s WHERE id=%s",(user.password_hash, user.id))

def create_password_reset_token(email):
    user = User.from_row(
        db.fetchone("SELECT * FROM users WHERE email=%s LIMIT 1",(email.strip().lower(),)))

    if not user or not user.is_active:
        return None

    token, token_hash = generate_password_reset_token()
    expiry = password_reset_expiry()

    db.execute("""
        UPDATE users
        SET reset_token_hash=%s,
            reset_token_expires_at=%s
        WHERE id=%s
        """,
        (
            token_hash,
            expiry,
            user.id
        )
    )

    return token


def reset_password_with_token(token, new_password):
    token_hash = hash_token(token)

    user = User.from_row(db.fetchone("""
            SELECT * FROM users
            WHERE reset_token_hash=%s
            LIMIT 1
            """,
            (token_hash,)
        )
    )

    if not user:
        return False

    if is_token_expired(user.reset_token_expires_at):
        return False

    user.set_password(new_password)
    db.execute("""
        UPDATE users
        SET password_hash=%s,
            reset_token_hash=NULL,
            reset_token_expires_at=NULL
        WHERE id=%s
        """,
        (
            user.password_hash,
            user.id
        )
    )

    return True
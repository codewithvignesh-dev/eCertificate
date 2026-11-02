from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from ..extensions import db

class User(UserMixin):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.password_hash = kwargs.get("password_hash")
        self.role = kwargs.get("role", "staff")
        self._is_active = bool(kwargs.get("is_active", 0))
        self.email_verified = bool(kwargs.get("email_verified", 0))
        self.created_at = kwargs.get("created_at")
        self.last_login_at = kwargs.get("last_login_at")
        self.reset_token_hash = kwargs.get("reset_token_hash")
        self.reset_token_expires_at = kwargs.get("reset_token_expires_at")

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = bool(value)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return bool(self.password_hash) and check_password_hash(self.password_hash, password)

    def update_last_login(self):
        db.execute("UPDATE users SET last_login_at=NOW() WHERE id=%s", (self.id,))

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_manager(self):
        return self.role == "manager"

    @property
    def is_staff(self):
        return self.role == "staff"

    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        return cls(**dict(row))

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.email}>"
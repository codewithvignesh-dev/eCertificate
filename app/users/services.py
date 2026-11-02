from ..extensions import db
from ..models import User

def get_users():
    return [User.from_row(r) for r in db.fetchall("SELECT * FROM users ORDER BY created_at DESC")]

def get_user(user_id):
    return User.from_row(db.fetchone("SELECT * FROM users WHERE id=%s LIMIT 1", (user_id,)))

def create_user(name, email, password, role="staff"):
    user = User(name=name.strip(), email=email.strip().lower(), role=role, is_active=1, email_verified=0)
    user.set_password(password)
    user_id = db.execute(
        "INSERT INTO users (name,email,password_hash,role,is_active,email_verified) VALUES (%s,%s,%s,%s,%s,%s)",
        (user.name,user.email,user.password_hash,user.role,1,0)
    )
    user.id=user_id
    return user

def update_user(user, name, email, role, is_active, password=None):
    user.name=name.strip(); user.email=email.strip().lower(); user.role=role; user.is_active=1 if is_active else 0
    if password: user.set_password(password)
    if password:
        db.execute("UPDATE users SET name=%s,email=%s,role=%s,is_active=%s,password_hash=%s WHERE id=%s",
                   (user.name,user.email,user.role,user.is_active,user.password_hash,user.id))
    else:
        db.execute("UPDATE users SET name=%s,email=%s,role=%s,is_active=%s WHERE id=%s",
                   (user.name,user.email,user.role,user.is_active,user.id))
    return user

def toggle_user_status(user):
    user.is_active = 0 if user.is_active else 1
    db.execute("UPDATE users SET is_active=%s WHERE id=%s",(user.is_active,user.id))
    return user

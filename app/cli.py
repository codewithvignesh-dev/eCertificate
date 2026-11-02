import click
from .extensions import db
from .models import User

def register_cli(app):
    @app.cli.command("create-admin")
    @click.option("--name",prompt=True)
    @click.option("--email",prompt=True)
    @click.option("--password",prompt=True,hide_input=True,confirmation_prompt=True)
    def create_admin(name,email,password):
        email=email.strip().lower()
        user=User.from_row(db.fetchone("SELECT * FROM users WHERE email=%s LIMIT 1",(email,)))
        if user:
            user.set_password(password)
            db.execute("UPDATE users SET role='admin',is_active=1,email_verified=1,password_hash=%s WHERE id=%s",(user.password_hash,user.id))
            click.echo(f"Existing user {email} promoted to admin."); return
        user=User(name=name.strip(),email=email,role="admin",is_active=1,email_verified=1)
        user.set_password(password)
        db.execute("INSERT INTO users (name,email,password_hash,role,is_active,email_verified) VALUES (%s,%s,%s,'admin',1,1)",(user.name,user.email,user.password_hash))
        click.echo(f"Admin account created for {email}.")

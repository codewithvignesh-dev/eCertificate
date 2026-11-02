from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from ..extensions import db

class UserCreateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    role = SelectField(
        "Role",
        choices=[
            ("staff", "Staff"),
            ("manager", "Manager"),
            ("admin", "Admin")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Create User")

    def validate_email(self, field):
        email = field.data.strip().lower()
        if db.fetchone("SELECT id FROM users WHERE email=%s LIMIT 1", (email,)):
            raise ValidationError("An account with this email already exists.")

class UserEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("New Password", validators=[Optional(), Length(min=8, max=128)])
    confirm_password = PasswordField("Confirm Password", validators=[Optional(), EqualTo("password")])
    role = SelectField(
        "Role",
        choices=[
            ("staff", "Staff"),
            ("manager", "Manager"),
            ("admin", "Admin")
        ],
        validators=[DataRequired()]
    )
    status = SelectField(
        "Status",
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Update User")

    def __init__(self, user_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id

    def validate_email(self, field):
        email = field.data.strip().lower()
        user = db.fetchone("SELECT id FROM users WHERE email=%s AND id<>%s LIMIT 1", (email, self.user_id))

        if user:
            raise ValidationError("An account with this email already exists.")
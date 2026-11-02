from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from ..extensions import db


class SignInForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=128)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class SignUpForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=2, max=150)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=128)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )
    submit = SubmitField("Create Account")

    def validate_email(self, field):
        email = field.data.strip().lower()

        if db.fetchone("SELECT id FROM users WHERE email=%s LIMIT 1", (email,)):
            raise ValidationError(
                "An account with this email already exists."
            )


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)]
    )
    submit = SubmitField("Send Reset Link")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=8, max=128)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )
    submit = SubmitField("Reset Password")
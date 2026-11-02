from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class ProfileForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=2, max=150)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)]
    )
    submit = SubmitField("Save Changes")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired(), Length(min=8, max=128)]
    )
    new_password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=8, max=128)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("new_password")
        ]
    )
    submit = SubmitField("Change Password")

class DeleteAccountForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=128)]
    )
    submit = SubmitField("Delete Account")
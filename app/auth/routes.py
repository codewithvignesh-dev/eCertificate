from flask import current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import limiter
from . import auth
from .forms import ForgotPasswordForm, ResetPasswordForm, SignInForm, SignUpForm
from .services import (
    authenticate_user,
    create_password_reset_token,
    create_user,
    reset_password_with_token
)


@auth.route("/signin", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = SignInForm()

    if form.validate_on_submit():
        user = authenticate_user(
            form.email.data,
            form.password.data
        )

        if user:
            user.update_last_login()
            login_user(
                user,
                remember=form.remember.data,
                fresh=True
            )
            flash("Welcome back.", "success")
            return redirect(url_for("dashboard.index"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/signin.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
@limiter.limit("5 per hour", methods=["POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = SignUpForm()

    if form.validate_on_submit():
        create_user(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )

        flash(
            "Account created successfully. You can now sign in.",
            "success"
        )
        return redirect(url_for("auth.signin"))

    return render_template("auth/signup.html", form=form)


@auth.route("/forgot-password", methods=["GET", "POST"])
@limiter.limit("5 per hour", methods=["POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        token = create_password_reset_token(form.email.data)

        if token:
            reset_url = url_for(
                "auth.reset_password",
                token=token,
                _external=True
            )
            # No email service is configured for this project yet, so the
            # reset link is logged server-side. Once SMTP/an email
            # provider is wired up, replace this with an actual email send.
            current_app.logger.info(
                "Password reset requested for %s: %s",
                form.email.data.strip().lower(),
                reset_url
            )

        flash(
            "If an account exists with that email, a password reset link "
            "has been generated.",
            "info"
        )
        return redirect(url_for("auth.signin"))

    return render_template(
        "auth/forgot_password.html",
        form=form
    )


@auth.route("/reset-password/<token>", methods=["GET", "POST"])
@limiter.limit("5 per hour", methods=["POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        if reset_password_with_token(token, form.password.data):
            flash(
                "Your password has been reset. You can now sign in.",
                "success"
            )
            return redirect(url_for("auth.signin"))

        flash(
            "This password reset link is invalid or has expired. "
            "Please request a new one.",
            "danger"
        )
        return redirect(url_for("auth.forgot_password"))

    return render_template(
        "auth/reset_password.html",
        form=form,
        token=token
    )


@auth.get("/signout")
@login_required
def signout():
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("auth.signin"))
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from ..extensions import db
from ..models import User
from ..utils.decorators import admin_required
from . import users
from .forms import UserCreateForm, UserEditForm
from .services import create_user, get_user, get_users, toggle_user_status, update_user

@users.get("/")
@login_required
@admin_required
def index():
    users_list = get_users()
    return render_template("users/index.html", users=users_list)

@users.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    form = UserCreateForm()

    if form.validate_on_submit():
        create_user(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data
        )
        flash("User created successfully.", "success")
        return redirect(url_for("users.index"))

    return render_template("users/create.html", form=form)

@users.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit(user_id):
    user = get_user(user_id)

    if not user:
        return redirect(url_for("users.index"))

    form = UserEditForm(user_id=user.id, obj=user)

    if form.validate_on_submit():
        update_user(
            user=user,
            name=form.name.data,
            email=form.email.data,
            role=form.role.data,
            is_active=form.status.data == "active",
            password=form.password.data or None
        )
        flash("User updated successfully.", "success")
        return redirect(url_for("users.index"))

    if not form.is_submitted():
        form.status.data = "active" if user.is_active else "inactive"

    return render_template("users/edit.html", form=form, user=user)

@users.post("/toggle/<int:user_id>")
@login_required
@admin_required
def toggle(user_id):
    user = get_user(user_id)

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("users.index"))

    if user.id == current_user.id:
        flash("You cannot deactivate your own account.", "warning")
        return redirect(url_for("users.index"))

    toggle_user_status(user)
    flash("User status updated successfully.", "success")
    return redirect(url_for("users.index"))
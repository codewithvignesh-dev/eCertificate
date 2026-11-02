from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user
from ..extensions import db
from . import profile
from .forms import ChangePasswordForm, DeleteAccountForm, ProfileForm

@profile.route("/", methods=["GET","POST"])
@login_required
def index():
    form=ProfileForm(obj=current_user)
    if form.validate_on_submit():
        email=form.email.data.strip().lower()
        existing=db.fetchone("SELECT id FROM users WHERE email=%s AND id<>%s LIMIT 1",(email,current_user.id))
        if existing:
            flash("An account with this email already exists.","danger")
            return render_template("profile/index.html",form=form)
        current_user.name=form.name.data.strip(); current_user.email=email
        db.execute("UPDATE users SET name=%s,email=%s WHERE id=%s",(current_user.name,current_user.email,current_user.id))
        flash("Profile updated successfully.","success")
        return redirect(url_for("profile.index"))
    return render_template("profile/index.html",form=form)

@profile.route("/change-password",methods=["GET","POST"])
@login_required
def change_password():
    form=ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.","danger")
            return render_template("profile/change_password.html",form=form)
        current_user.set_password(form.new_password.data)
        db.execute("UPDATE users SET password_hash=%s WHERE id=%s",(current_user.password_hash,current_user.id))
        logout_user()
        flash("Password changed successfully. Please sign in again.","success")
        return redirect(url_for("auth.signin"))
    return render_template("profile/change_password.html",form=form)

@profile.route("/delete-account",methods=["GET","POST"])
@login_required
def delete_account():
    form=DeleteAccountForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.password.data):
            flash("Password is incorrect.","danger")
            return render_template("profile/delete_account.html",form=form)
        if current_user.is_admin:
            count=db.fetchone("SELECT COUNT(*) AS count FROM users WHERE role='admin' AND is_active=1")["count"]
            if count<=1:
                flash("The last active administrator account cannot be deleted.","danger")
                return render_template("profile/delete_account.html",form=form)
        user_id=current_user.id
        logout_user()
        db.execute("DELETE FROM users WHERE id=%s",(user_id,))
        flash("Your account has been deleted.","success")
        return redirect(url_for("main.landing"))
    return render_template("profile/delete_account.html",form=form)

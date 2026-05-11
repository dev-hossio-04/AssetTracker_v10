from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.models.audit_log import AuditLog
from app import db
import socket

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username, active=True).first()

        if user and user.check_password(password):
            login_user(user)
            log = AuditLog(
                username=user.username,
                action="Login",
                module="Authentication",
                record_id=str(user.id),
                ip_address=request.remote_addr,
                pc_name=socket.gethostname()
            )
            db.session.add(log)
            db.session.commit()
            return redirect(url_for("main.dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    username = current_user.username
    log = AuditLog(
        username=username,
        action="Logout",
        module="Authentication",
        ip_address=request.remote_addr,
        pc_name=socket.gethostname()
    )
    db.session.add(log)
    db.session.commit()
    logout_user()
    return redirect(url_for("auth.login"))

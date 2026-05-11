from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app import db
from app.models.asset import Asset
from app.models.staff import Staff
from app.models.transaction import Transaction
from app.models.audit_log import AuditLog
import socket
import os
from datetime import datetime
from openpyxl import Workbook
from functools import wraps
from flask import abort
from app.models.user import User


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

main = Blueprint("main", __name__)

def write_audit(action, module, record_id=None):
    log = AuditLog(
        username=current_user.username if current_user.is_authenticated else None,
        action=action,
        module=module,
        record_id=str(record_id) if record_id else None,
        ip_address=request.remote_addr,
        pc_name=socket.gethostname()
    )
    db.session.add(log)

@main.route("/")
def home():
    return redirect(url_for("auth.login"))

@main.route("/dashboard")
@login_required
def dashboard():
    total_assets = Asset.query.count()
    available = Asset.query.filter_by(status="Available").count()
    checked_out = Asset.query.filter_by(status="Checked Out").count()
    repair = Asset.query.filter_by(status="Under Repair").count()
    recent = Transaction.query.order_by(Transaction.timestamp.desc()).limit(10).all()
    return render_template(
        "dashboard.html",
        total_assets=total_assets,
        available=available,
        checked_out=checked_out,
        repair=repair,
        recent=recent
    )

@main.route("/assets")
@login_required
def assets():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()

    query = Asset.query

    if q:
        search = f"%{q}%"
        query = query.filter(
            (Asset.asset_id.like(search)) |
            (Asset.serial_number.like(search)) |
            (Asset.brand.like(search)) |
            (Asset.model.like(search)) |
            (Asset.assigned_to.like(search))
        )

    if status:
        query = query.filter_by(status=status)

    asset_list = query.order_by(Asset.asset_id.asc()).all()
    return render_template("assets.html", assets=asset_list, q=q, status=status)

@main.route("/assets/add", methods=["GET", "POST"])
@login_required
def add_asset():
    if request.method == "POST":
        asset_id = request.form.get("asset_id", "").strip()
        serial_number = request.form.get("serial_number", "").strip()

        if Asset.query.filter_by(asset_id=asset_id).first():
            flash("Asset ID already exists.", "danger")
            return redirect(url_for("main.add_asset"))

        if serial_number and Asset.query.filter_by(serial_number=serial_number).first():
            flash("Serial number already exists.", "danger")
            return redirect(url_for("main.add_asset"))

        asset = Asset(
            asset_id=asset_id,
            asset_type=request.form.get("asset_type", "").strip(),
            brand=request.form.get("brand", "").strip(),
            model=request.form.get("model", "").strip(),
            serial_number=serial_number,
            status=request.form.get("status", "Available"),
            location=request.form.get("location", "").strip(),
            notes=request.form.get("notes", "").strip()
        )
        db.session.add(asset)
        write_audit("Add Asset", "Assets", asset_id)
        db.session.commit()
        flash("Asset added successfully.", "success")
        return redirect(url_for("main.assets"))

    return render_template("asset_form.html")

@main.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if request.method == "POST":
        asset_id = request.form.get("asset_id", "").strip()
        assigned_to = request.form.get("assigned_to", "").strip()
        event_name = request.form.get("event_name", "").strip()
        authorized_by = request.form.get("authorized_by", "").strip()
        remarks = request.form.get("remarks", "").strip()

        asset = Asset.query.filter_by(asset_id=asset_id).first()

        if not asset:
            flash("Asset not found.", "danger")
            return redirect(url_for("main.checkout"))

        if asset.status not in ["Available", "Returned"]:
            flash(f"Asset cannot be checked out. Current status: {asset.status}", "danger")
            return redirect(url_for("main.checkout"))

        asset.status = "Checked Out"
        asset.assigned_to = assigned_to

        tx = Transaction(
            asset_id=asset.asset_id,
            action_type="Check-Out",
            assigned_to=assigned_to,
            event_name=event_name,
            authorized_by=authorized_by,
            performed_by=current_user.username,
            pc_name=socket.gethostname(),
            remarks=remarks
        )

        db.session.add(tx)
        write_audit("Check-Out Asset", "Transactions", asset.asset_id)
        db.session.commit()
        flash("Asset checked out successfully.", "success")
        return redirect(url_for("main.dashboard"))

    assets = Asset.query.filter(Asset.status.in_(["Available", "Returned"])).order_by(Asset.asset_id.asc()).all()
    staff = Staff.query.filter_by(active=True).order_by(Staff.full_name.asc()).all()
    return render_template("checkout.html", assets=assets, staff=staff)

@main.route("/checkin", methods=["GET", "POST"])
@login_required
def checkin():
    if request.method == "POST":
        asset_id = request.form.get("asset_id", "").strip()
        authorized_by = request.form.get("authorized_by", "").strip()
        condition = request.form.get("condition", "Returned")
        remarks = request.form.get("remarks", "").strip()

        asset = Asset.query.filter_by(asset_id=asset_id).first()

        if not asset:
            flash("Asset not found.", "danger")
            return redirect(url_for("main.checkin"))

        if asset.status != "Checked Out":
            flash(f"Asset is not currently checked out. Current status: {asset.status}", "danger")
            return redirect(url_for("main.checkin"))

        asset.status = "Available" if condition == "Returned" else condition
        old_assigned = asset.assigned_to
        asset.assigned_to = None if asset.status == "Available" else asset.assigned_to

        tx = Transaction(
            asset_id=asset.asset_id,
            action_type="Check-In",
            assigned_to=old_assigned,
            authorized_by=authorized_by,
            performed_by=current_user.username,
            pc_name=socket.gethostname(),
            remarks=remarks
        )

        db.session.add(tx)
        write_audit("Check-In Asset", "Transactions", asset.asset_id)
        db.session.commit()
        flash("Asset checked in successfully.", "success")
        return redirect(url_for("main.dashboard"))

    assets = Asset.query.filter_by(status="Checked Out").order_by(Asset.asset_id.asc()).all()
    return render_template("checkin.html", assets=assets)

@main.route("/transactions")
@login_required
def transactions():
    txs = Transaction.query.order_by(Transaction.timestamp.desc()).limit(300).all()
    return render_template("transactions.html", transactions=txs)

@main.route("/audit")
@login_required
def audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(300).all()
    return render_template("audit.html", logs=logs)

@main.route("/export/assets")
@login_required
def export_assets():
    rows = Asset.query.order_by(Asset.asset_id.asc()).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Assets"

    headers = [
        "Asset ID", "Type", "Brand", "Model", "Serial Number",
        "Status", "Assigned To", "Location", "Notes", "Created At"
    ]
    ws.append(headers)

    for a in rows:
        ws.append([
            a.asset_id,
            a.asset_type,
            a.brand,
            a.model,
            a.serial_number,
            a.status,
            a.assigned_to,
            a.location,
            a.notes,
            str(a.created_at)
        ])

    export_dir = os.path.join(os.getcwd(), "exports")
    os.makedirs(export_dir, exist_ok=True)

    path = os.path.join(
        export_dir,
        f"assets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    wb.save(path)

    return send_file(path, as_attachment=True)

@main.route("/users")
@login_required
@admin_required
def users():
    user_list = User.query.order_by(User.username.asc()).all()
    return render_template("users.html", users=user_list)


@main.route("/users/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():
    if request.method == "POST":
        username = request.form.get("username").strip()
        full_name = request.form.get("full_name").strip()
        password = request.form.get("password")
        role = request.form.get("role")
        active = True if request.form.get("active") == "on" else False

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("main.add_user"))

        user = User(
            username=username,
            full_name=full_name,
            role=role,
            active=active
        )
        user.set_password(password)

        db.session.add(user)
        write_audit("Add User", "Users", username)
        db.session.commit()

        flash("User created successfully.", "success")
        return redirect(url_for("main.users"))

    return render_template("user_form.html", user=None)


@main.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.full_name = request.form.get("full_name").strip()
        user.role = request.form.get("role")
        user.active = True if request.form.get("active") == "on" else False

        new_password = request.form.get("password")
        if new_password:
            user.set_password(new_password)

        write_audit("Edit User", "Users", user.username)
        db.session.commit()

        flash("User updated successfully.", "success")
        return redirect(url_for("main.users"))

    return render_template("user_form.html", user=user)

@main.route("/assets/edit/<int:asset_id>", methods=["GET", "POST"])
@login_required
def edit_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)

    if request.method == "POST":
        asset.asset_type = request.form.get("asset_type").strip()
        asset.brand = request.form.get("brand").strip()
        asset.model = request.form.get("model").strip()
        asset.serial_number = request.form.get("serial_number").strip()
        asset.status = request.form.get("status")
        asset.assigned_to = request.form.get("assigned_to").strip()
        asset.location = request.form.get("location").strip()
        asset.notes = request.form.get("notes").strip()
        asset.condition = request.form.get("condition").strip()
        asset.purpose = request.form.get("purpose").strip()
        asset.notes = request.form.get("notes").strip()

        write_audit("Edit Asset", "Assets", asset.asset_id)
        db.session.commit()

        flash("Asset updated successfully.", "success")
        return redirect(url_for("main.assets"))

    return render_template("asset_edit.html", asset=asset)
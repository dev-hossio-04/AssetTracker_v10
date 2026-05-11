from datetime import datetime
from app import db

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=True)
    action = db.Column(db.String(150), nullable=False)
    module = db.Column(db.String(100), nullable=True)
    record_id = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(100), nullable=True)
    pc_name = db.Column(db.String(150), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

from datetime import datetime
from app import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(80), nullable=False)
    action_type = db.Column(db.String(50), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=True)
    event_name = db.Column(db.String(150), nullable=True)
    authorized_by = db.Column(db.String(150), nullable=True)
    performed_by = db.Column(db.String(100), nullable=True)
    pc_name = db.Column(db.String(150), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

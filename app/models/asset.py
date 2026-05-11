from datetime import datetime
from app import db

class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(80), unique=True, nullable=False)
    asset_type = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    serial_number = db.Column(db.String(150), unique=True, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Available")
    assigned_to = db.Column(db.String(80), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)
    condition = db.Column(db.String(100), nullable=True)
    purpose = db.Column(db.Text, nullable=True)
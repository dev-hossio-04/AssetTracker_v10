from app import db

class Staff(db.Model):
    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(50), unique=True, nullable=True)
    full_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    active = db.Column(db.Boolean, default=True)

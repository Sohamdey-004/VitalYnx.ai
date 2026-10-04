from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    phone_verified = db.Column(db.Boolean, default=False, nullable=False)
    location_label = db.Column(db.String(180))
    location_latitude = db.Column(db.Float)
    location_longitude = db.Column(db.Float)
    gender = db.Column(db.String(30))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    hereditary_conditions = db.Column(db.JSON, default=list)
    current_health_issues = db.Column(db.JSON, default=list)
    wellness_preferences = db.Column(db.JSON, default=list)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(30))
    emergency_contact_relationship = db.Column(db.String(80))
    profile_completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    readings = db.relationship('Reading', backref='user', lazy=True, cascade='all, delete-orphan')
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
    @property
    def bmi(self): return round(self.weight / ((self.height / 100) ** 2), 1) if self.height and self.weight else None

class VerificationChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    email_code_hash = db.Column(db.String(255), nullable=False)
    phone_code_hash = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    pulse = db.Column(db.Integer, nullable=False)
    spo2 = db.Column(db.Integer, nullable=False)
    systolic = db.Column(db.Integer, nullable=False)
    diastolic = db.Column(db.Integer, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    ecg_data = db.Column(db.JSON, default=list)
    signal_quality = db.Column(db.String(20), default='good')
    risk_level = db.Column(db.String(20), nullable=False)
    risk_score = db.Column(db.Integer, nullable=False)
    ai_analysis = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(16), nullable=False, default='demo', server_default='demo')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

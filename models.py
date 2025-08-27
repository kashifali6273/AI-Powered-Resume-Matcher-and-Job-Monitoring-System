from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin  # 👈 Add this
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = "user"  # ✅ Add this

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


class Resume(db.Model):
    __tablename__ = "resume"  # ✅ Add this

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class MonitoringRule(db.Model):
    __tablename__ = "monitoring_rule"  # ✅ Recommended but optional

    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resume = db.relationship("Resume", backref="monitoring_rules")
    user = db.relationship("User", backref="monitoring_rules")


class WatchlistMatch(db.Model):
    __tablename__ = "watchlist_match"  # ✅ Recommended but optional

    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200))
    company = db.Column(db.String(200))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    match_score = db.Column(db.Float)
    link = db.Column(db.String(500))
    found_at = db.Column(db.DateTime, default=datetime.utcnow)

    rule_id = db.Column(db.Integer, db.ForeignKey("monitoring_rule.id"), nullable=False)
    monitoring_rule = db.relationship("MonitoringRule", backref="matches")

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from bcrypt import hashpw, gensalt, checkpw

db = SQLAlchemy()

# Guest sessions are ordinary user rows whose email uses this reserved domain
GUEST_EMAIL_DOMAIN = 'guest.intellipattern.local'

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    study_sessions = db.relationship('StudySession', backref='user', lazy=True, cascade='all, delete-orphan')
    performance_records = db.relationship('PerformanceRecord', backref='user', lazy=True, cascade='all, delete-orphan')
    wellness_tracking = db.relationship('WellnessTracking', backref='user', lazy=True, cascade='all, delete-orphan')
    
    @property
    def is_guest(self):
        """True for temporary guest sessions"""
        return self.email.endswith('@' + GUEST_EMAIL_DOMAIN)

    def set_password(self, password):
        """Hash and set password"""
        salt = gensalt()
        self.password_hash = hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.email}>'

class StudySession(db.Model):
    """Study sessions linked to users"""
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    start_time = db.Column(db.String(10), nullable=False)  # HH:MM format
    end_time = db.Column(db.String(10), nullable=False)    # HH:MM format
    study_method = db.Column(db.String(50), nullable=False)
    difficulty_level = db.Column(db.Integer, nullable=False)  # 1-5 scale
    focus_rating = db.Column(db.Integer, nullable=False)     # 1-5 scale
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<StudySession {self.subject} - {self.duration}min>'

class PerformanceRecord(db.Model):
    """Performance records linked to users"""
    __tablename__ = 'performance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    assessment_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD format
    topics_covered = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    @property
    def percentage(self):
        """Calculate percentage score"""
        return round((self.score / self.max_score) * 100, 1)
    
    def __repr__(self):
        return f'<PerformanceRecord {self.subject} - {self.percentage}%>'

class WellnessTracking(db.Model):
    """Wellness tracking linked to users"""
    __tablename__ = 'wellness_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    date = db.Column(db.String(10), nullable=False, index=True)  # YYYY-MM-DD format
    sleep_hours = db.Column(db.Float, nullable=False)
    stress_level = db.Column(db.Integer, nullable=False)   # 1-5 scale
    mood_rating = db.Column(db.Integer, nullable=False)    # 1-5 scale
    exercise_minutes = db.Column(db.Integer, default=0)
    caffeine_intake = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WellnessTracking {self.date} - {self.sleep_hours}h sleep>'

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.set_password(password)
        self.is_admin = is_admin
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    height = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(5, 2))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('male', 'female', 'other'))
    activity_level = db.Column(db.Enum('sedentary', 'light', 'moderate', 'active', 'very_active'))
    bmr = db.Column(db.Numeric(8, 2))
    tdee = db.Column(db.Numeric(8, 2))
    calorie_target = db.Column(db.Numeric(8, 2))
    protein_target = db.Column(db.Numeric(6, 2))
    fat_target = db.Column(db.Numeric(6, 2))
    carb_target = db.Column(db.Numeric(6, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'height': float(self.height) if self.height else None,
            'weight': float(self.weight) if self.weight else None,
            'age': self.age,
            'gender': self.gender,
            'activity_level': self.activity_level,
            'bmr': float(self.bmr) if self.bmr else None,
            'tdee': float(self.tdee) if self.tdee else None,
            'calorie_target': float(self.calorie_target) if self.calorie_target else None,
            'protein_target': float(self.protein_target) if self.protein_target else None,
            'fat_target': float(self.fat_target) if self.fat_target else None,
            'carb_target': float(self.carb_target) if self.carb_target else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 
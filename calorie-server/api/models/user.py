from . import db
from datetime import datetime

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(50))
    avatar_url = db.Column(db.String(255))
    session_key = db.Column(db.String(50))  # 添加session_key字段
    last_login = db.Column(db.DateTime)  # 添加最后登录时间字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联 - 使用字符串引用而不是直接引用类
    profile = db.relationship('UserProfile', backref='user', uselist=False)
    # 延迟加载关系，避免循环导入
    food_records = db.relationship('FoodRecord', backref='user', lazy='dynamic')
    feedbacks = db.relationship('UserFeedback', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.id}>'

class UserProfile(db.Model):
    """用户信息表"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    height = db.Column(db.Float)  # 身高(cm)
    weight = db.Column(db.Float)  # 体重(kg)
    age = db.Column(db.Integer)  # 年龄
    gender = db.Column(db.Enum('male', 'female', 'other', name='gender_types'))  # 性别
    activity_level = db.Column(db.Enum('sedentary', 'light', 'moderate', 'active', 'very_active', name='activity_level_types'))  # 活动量级别
    bmr = db.Column(db.Float)  # 基础代谢率
    tdee = db.Column(db.Float)  # 总能量消耗
    calorie_target = db.Column(db.Float)  # 目标热量
    protein_target = db.Column(db.Float)  # 蛋白质目标(g)
    fat_target = db.Column(db.Float)  # 脂肪目标(g)
    carb_target = db.Column(db.Float)  # 碳水目标(g)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserProfile {self.id}>'

class UserFeedback(db.Model):
    """用户反馈表"""
    __tablename__ = 'user_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    feedback_type = db.Column(db.Enum('bug', 'suggestion', 'complaint', 'other', name='feedback_type'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    contact_info = db.Column(db.String(100))
    status = db.Column(db.Enum('pending', 'processing', 'resolved', 'rejected', name='feedback_status'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserFeedback {self.id}>' 
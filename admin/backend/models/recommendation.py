from . import db
from datetime import datetime

class RecommendationAlgorithmParam(db.Model):
    __tablename__ = 'recommendation_algorithm_params'
    
    id = db.Column(db.Integer, primary_key=True)
    param_name = db.Column(db.String(100), nullable=False)
    param_value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'param_name': self.param_name,
            'param_value': self.param_value,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RecommendationRule(db.Model):
    __tablename__ = 'recommendation_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    rule_name = db.Column(db.String(100), nullable=False)
    calorie_ratio = db.Column(db.Numeric(5, 2), comment='热量分配比例')
    protein_ratio = db.Column(db.Numeric(5, 2), comment='蛋白质分配比例')
    fat_ratio = db.Column(db.Numeric(5, 2), comment='脂肪分配比例')
    carb_ratio = db.Column(db.Numeric(5, 2), comment='碳水分配比例')
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_name': self.rule_name,
            'calorie_ratio': float(self.calorie_ratio) if self.calorie_ratio else None,
            'protein_ratio': float(self.protein_ratio) if self.protein_ratio else None,
            'fat_ratio': float(self.fat_ratio) if self.fat_ratio else None,
            'carb_ratio': float(self.carb_ratio) if self.carb_ratio else None,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RecommendationResult(db.Model):
    __tablename__ = 'recommendation_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rule_id = db.Column(db.Integer, db.ForeignKey('recommendation_rules.id'))
    result_data = db.Column(db.JSON, nullable=False, comment='推荐结果数据')
    status = db.Column(db.Enum('pending', 'approved', 'rejected', 'adjusted'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='recommendation_results')
    rule = db.relationship('RecommendationRule', backref='recommendation_results')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'rule_id': self.rule_id,
            'result_data': self.result_data,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 
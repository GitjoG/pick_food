from . import db
from datetime import datetime

class NutritionGoalStatistics(db.Model):
    __tablename__ = 'nutrition_goal_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    calorie_target = db.Column(db.Numeric(8, 2))
    calorie_actual = db.Column(db.Numeric(8, 2))
    protein_target = db.Column(db.Numeric(6, 2))
    protein_actual = db.Column(db.Numeric(6, 2))
    fat_target = db.Column(db.Numeric(6, 2))
    fat_actual = db.Column(db.Numeric(6, 2))
    carb_target = db.Column(db.Numeric(6, 2))
    carb_actual = db.Column(db.Numeric(6, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='nutrition_statistics')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'calorie_target': float(self.calorie_target) if self.calorie_target else None,
            'calorie_actual': float(self.calorie_actual) if self.calorie_actual else None,
            'protein_target': float(self.protein_target) if self.protein_target else None,
            'protein_actual': float(self.protein_actual) if self.protein_actual else None,
            'fat_target': float(self.fat_target) if self.fat_target else None,
            'fat_actual': float(self.fat_actual) if self.fat_actual else None,
            'carb_target': float(self.carb_target) if self.carb_target else None,
            'carb_actual': float(self.carb_actual) if self.carb_actual else None,
            'created_at': self.created_at.isoformat()
        } 
from . import db
from datetime import datetime

class FoodRecord(db.Model):
    """食物记录表"""
    __tablename__ = 'food_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'))  # 可为空，自定义食物时
    meal_type = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack', name='meal_types'), nullable=False)
    custom_food_name = db.Column(db.String(100))  # 自定义食物名称
    calories = db.Column(db.Float, nullable=False)  # 热量(千卡)
    protein = db.Column(db.Float, nullable=False)  # 蛋白质(g)
    fat = db.Column(db.Float, nullable=False)  # 脂肪(g)
    carbs = db.Column(db.Float, nullable=False)  # 碳水化合物(g)
    record_date = db.Column(db.Date, nullable=False)  # 记录日期
    record_time = db.Column(db.Time, nullable=False)  # 记录时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<FoodRecord {self.id}>'

class DailyNutritionSummary(db.Model):
    """每日营养摄入汇总模型"""
    __tablename__ = 'daily_nutrition_summaries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date, default=datetime.utcnow().date)
    total_calorie = db.Column(db.Float, default=0)  # 总热量(kcal)
    total_protein = db.Column(db.Float, default=0)  # 总蛋白质(g)
    total_fat = db.Column(db.Float, default=0)  # 总脂肪(g)
    total_carb = db.Column(db.Float, default=0)  # 总碳水化合物(g)
    remaining_calorie = db.Column(db.Float)  # 剩余热量(kcal)
    remaining_protein = db.Column(db.Float)  # 剩余蛋白质(g)
    remaining_fat = db.Column(db.Float)  # 剩余脂肪(g)
    remaining_carb = db.Column(db.Float)  # 剩余碳水化合物(g)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DailyNutritionSummary {self.date}>' 
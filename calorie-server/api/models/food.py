from . import db
from datetime import datetime

class FoodItem(db.Model):
    """菜品表"""
    __tablename__ = 'food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)  # 热量(千卡)
    protein = db.Column(db.Float, nullable=False)  # 蛋白质(g)
    fat = db.Column(db.Float, nullable=False)  # 脂肪(g)
    carbs = db.Column(db.Float, nullable=False)  # 碳水化合物(g)
    image_url = db.Column(db.String(255))  # 菜品图片URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联 - 使用字符串引用
    food_records = db.relationship('FoodRecord', backref='food_item', lazy='dynamic')
    
    def __repr__(self):
        return f'<FoodItem {self.name}>'

class FoodCategory(db.Model):
    """食物分类模型"""
    __tablename__ = 'food_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<FoodCategory {self.name}>'

# 食物与分类的多对多关系
food_category_association = db.Table('food_category_association',
    db.Column('food_id', db.Integer, db.ForeignKey('foods.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('food_categories.id'))
) 
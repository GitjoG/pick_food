from . import db
from datetime import datetime

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    food_items = db.relationship('FoodItem', backref='restaurant', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
           
            'food_count': len(self.food_items),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbs = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    food_records = db.relationship('FoodRecord', backref='food_item')
    
    def to_dict(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'calories': self.calories,
            'protein': self.protein,
            'fat': self.fat,
            'carbs': self.carbs,
            'image_url': self.image_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class FoodRecord(db.Model):
    __tablename__ = 'food_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'))
    meal_type = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack'), nullable=False)
    custom_food_name = db.Column(db.String(100))
    calories = db.Column(db.Numeric(8, 2), nullable=False)
    protein = db.Column(db.Numeric(6, 2), nullable=False)
    fat = db.Column(db.Numeric(6, 2), nullable=False)
    carbs = db.Column(db.Numeric(6, 2), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    record_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'food_item_id': self.food_item_id,
            'meal_type': self.meal_type,
            'custom_food_name': self.custom_food_name,
            'calories': float(self.calories),
            'protein': float(self.protein),
            'fat': float(self.fat),
            'carbs': float(self.carbs),
            'record_date': self.record_date.isoformat(),
            'record_time': self.record_time.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 
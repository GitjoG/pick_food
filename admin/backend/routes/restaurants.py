from flask import Blueprint, jsonify, request
from models import db
from models.restaurant import Restaurant, FoodItem
from sqlalchemy import desc

restaurants_bp = Blueprint('restaurants', __name__)

# 添加调试装饰器
def debug_route(f):
    def wrapper(*args, **kwargs):
        print(f"Accessing route: {request.path}")
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# 获取餐厅列表
@restaurants_bp.route('/restaurants/list', methods=['GET'])
@debug_route
def get_restaurants_list():
    print("Processing get_restaurants_list request")  # 添加调试日志
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    query = Restaurant.query
    if search:
        query = query.filter(Restaurant.name.ilike(f'%{search}%'))
    
    pagination = query.order_by(desc(Restaurant.created_at)).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
        'items': [restaurant.to_dict() for restaurant in pagination.items]
    })

# 创建餐厅
@restaurants_bp.route('/restaurants', methods=['POST'])
@debug_route
def create_restaurant():
    data = request.json
    restaurant = Restaurant(
        name=data['name'],
       
    )
    db.session.add(restaurant)
    db.session.commit()
    return jsonify(restaurant.to_dict()), 201

# 获取餐厅详情
@restaurants_bp.route('/restaurants/<int:id>', methods=['GET'])
@debug_route
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify(restaurant.to_dict())

# 更新餐厅信息
@restaurants_bp.route('/restaurants/<int:id>', methods=['PUT'])
@debug_route
def update_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    data = request.json
    
    if data.get('name'):
        restaurant.name = data['name']
   
    
    db.session.commit()
    return jsonify(restaurant.to_dict())

# 删除餐厅
@restaurants_bp.route('/restaurants/<int:id>', methods=['DELETE'])
@debug_route
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    
    # 删除关联的菜品
    FoodItem.query.filter_by(restaurant_id=id).delete()
    
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({'message': '删除成功'})

# 获取餐厅菜品列表
@restaurants_bp.route('/restaurants/<int:id>/menu', methods=['GET'])
@debug_route
def get_restaurant_menu(id):
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify([item.to_dict() for item in restaurant.food_items])

# 添加菜品
@restaurants_bp.route('/restaurants/<int:id>/menu', methods=['POST'])
@debug_route
def add_food_item(id):
    restaurant = Restaurant.query.get_or_404(id)
    data = request.json
    
    food_item = FoodItem(
        restaurant_id=id,
        name=data['name'],
        calories=data.get('calories', 0),
        protein=data.get('protein', 0),
        fat=data.get('fat', 0),
        carbs=data.get('carbs', 0),
        image_url=data.get('image_url', '')
    )
    
    db.session.add(food_item)
    db.session.commit()
    return jsonify(food_item.to_dict()), 201

# 更新菜品
@restaurants_bp.route('/restaurants/<int:restaurant_id>/menu/<int:food_id>', methods=['PUT'])
@debug_route
def update_food_item(restaurant_id, food_id):
    food_item = FoodItem.query.filter_by(id=food_id, restaurant_id=restaurant_id).first_or_404()
    data = request.json
    
    if data.get('name'):
        food_item.name = data['name']
    if data.get('calories') is not None:
        food_item.calories = data['calories']
    if data.get('protein') is not None:
        food_item.protein = data['protein']
    if data.get('fat') is not None:
        food_item.fat = data['fat']
    if data.get('carbs') is not None:
        food_item.carbs = data['carbs']
    if data.get('image_url') is not None:
        food_item.image_url = data['image_url']
    
    db.session.commit()
    return jsonify(food_item.to_dict())

# 删除菜品
@restaurants_bp.route('/restaurants/<int:restaurant_id>/menu/<int:food_id>', methods=['DELETE'])
@debug_route
def delete_food_item(restaurant_id, food_id):
    food_item = FoodItem.query.filter_by(id=food_id, restaurant_id=restaurant_id).first_or_404()
    db.session.delete(food_item)
    db.session.commit()
    return jsonify({'message': '删除成功'}) 
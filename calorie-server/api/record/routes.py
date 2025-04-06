from flask import Blueprint, request, jsonify, g, current_app
from functools import wraps
import jwt
import datetime
from ..models import db
from ..models.record import FoodRecord
from ..models.user import UserProfile

record_bp = Blueprint('record', __name__)

# 身份验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'code': 401, 'message': '未提供认证令牌'}), 401
        
        # 获取令牌
        token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
        
        try:
            # 解码令牌
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            g.user_id = payload.get('user_id')  # 用户ID存储在令牌的user_id字段中
        except jwt.ExpiredSignatureError:
            return jsonify({'code': 401, 'message': '令牌已过期'}), 401
        except (jwt.InvalidTokenError, Exception) as e:
            return jsonify({'code': 401, 'message': f'无效的令牌: {str(e)}'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# 辅助函数
def get_user_id():
    """获取当前用户ID"""
    return g.user_id

# 日期格式转换辅助函数
def format_date(date_str):
    """将YYYY-MM-DD格式的日期字符串转换为日期对象"""
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

# 处理用餐类型转换
def get_meal_type_db(meal_type):
    """将前端用餐类型转换为数据库枚举值"""
    meal_type_map = {
        '早餐': 'breakfast',
        '午餐': 'lunch',
        '晚餐': 'dinner',
        '下午茶': 'snack',
        '夜宵': 'snack'
    }
    return meal_type_map.get(meal_type, 'snack')

# 将数据库用餐类型转换回前端显示
def get_meal_type_display(db_meal_type):
    """将数据库枚举值转换为前端用餐类型"""
    meal_type_map = {
        'breakfast': '早餐',
        'lunch': '午餐',
        'dinner': '晚餐',
        'snack': '下午茶'  # 默认下午茶，也可以根据时间判断是下午茶还是夜宵
    }
    return meal_type_map.get(db_meal_type, '其他')

@record_bp.route('/add', methods=['POST'])
def add_record():
    """添加用户当日食物记录"""
    try:
        data = request.get_json()
        # 在测试阶段固定使用ID为1的测试用户
        user_id = 1
        
        # 验证必要参数
        required_fields = ['date', 'mealType', 'mealTime', 'food']
        for field in required_fields:
            if field not in data:
                return jsonify({'code': 1, 'message': f'缺少必要参数: {field}'})
        
        # 食物数据验证
        food = data['food']
        if not all(key in food for key in ['name', 'calories', 'protein', 'fat', 'carbs']):
            return jsonify({'code': 1, 'message': '食物数据不完整'})
        
        # 插入食物记录
        meal_type_db = get_meal_type_db(data['mealType'])
        record_time = datetime.datetime.strptime(data['mealTime'], '%H:%M').time()
        
        # 使用SQLAlchemy ORM创建记录
        record = FoodRecord(
            user_id=user_id,
            custom_food_name=food['name'],
            meal_type=meal_type_db,
            calories=food['calories'],
            protein=food['protein'],
            fat=food['fat'],
            carbs=food['carbs'],
            record_date=format_date(data['date']),
            record_time=record_time
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'code': 0, 
            'message': '添加成功',
            'data': {
                'recordId': record.id
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'message': f'添加失败: {str(e)}'})

@record_bp.route('/batchAdd', methods=['POST'])
@login_required
def batch_add_record():
    """批量添加用户食物记录"""
    try:
        data = request.get_json()
        user_id = get_user_id()
        
        # 验证必要参数
        required_fields = ['date', 'mealType', 'mealTime', 'foods']
        for field in required_fields:
            if field not in data:
                return jsonify({'code': 1, 'message': f'缺少必要参数: {field}'})
        
        # 检查foods是否为列表且不为空
        if not isinstance(data['foods'], list) or len(data['foods']) == 0:
            return jsonify({'code': 1, 'message': 'foods必须是非空列表'})
        
        meal_type_db = get_meal_type_db(data['mealType'])
        record_time = datetime.datetime.strptime(data['mealTime'], '%H:%M').time()
        record_date = format_date(data['date'])
        
        record_ids = []
        
        # 批量插入食物记录
        for food in data['foods']:
            if not all(key in food for key in ['name', 'calories', 'protein', 'fat', 'carbs']):
                continue  # 跳过不完整的食物数据
            
            record = FoodRecord(
                user_id=user_id,
                custom_food_name=food['name'],
                meal_type=meal_type_db,
                calories=food['calories'],
                protein=food['protein'],
                fat=food['fat'],
                carbs=food['carbs'],
                record_date=record_date,
                record_time=record_time
            )
            
            db.session.add(record)
            db.session.flush()  # 获取自增ID但不提交事务
            record_ids.append(record.id)
        
        db.session.commit()
        
        return jsonify({
            'code': 0, 
            'message': '批量添加成功',
            'data': {
                'recordIds': record_ids
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'message': f'批量添加失败: {str(e)}'})

@record_bp.route('/update', methods=['PUT'])
def update_record():
    """更新用户食物记录"""
    try:
        data = request.get_json()
        # 在测试阶段固定使用ID为1的测试用户
        user_id = 1
        
        # 验证必要参数
        if 'recordId' not in data:
            return jsonify({'code': 1, 'message': '缺少记录ID'})
        
        record_id = data['recordId']
        
        # 验证记录是否存在且属于当前用户
        record = FoodRecord.query.filter_by(id=record_id, user_id=user_id).first()
        if not record:
            return jsonify({'code': 1, 'message': '记录不存在或无权限修改'})
        
        # 更新记录字段
        if 'mealType' in data:
            record.meal_type = get_meal_type_db(data['mealType'])
        
        if 'mealTime' in data:
            record.record_time = datetime.datetime.strptime(data['mealTime'], '%H:%M').time()
        
        if 'food' in data and isinstance(data['food'], dict):
            food = data['food']
            
            if 'name' in food:
                record.custom_food_name = food['name']
            
            if 'calories' in food:
                record.calories = food['calories']
            
            if 'protein' in food:
                record.protein = food['protein']
            
            if 'fat' in food:
                record.fat = food['fat']
            
            if 'carbs' in food:
                record.carbs = food['carbs']
        
        db.session.commit()
        
        return jsonify({'code': 0, 'message': '更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'message': f'更新失败: {str(e)}'})

@record_bp.route('/delete', methods=['DELETE'])
def delete_record():
    """删除用户食物记录"""
    try:
        data = request.get_json()
        # 在测试阶段固定使用ID为1的测试用户
        user_id = 1
        
        record_id = data.get('recordId')
        if not record_id:
            return jsonify({'code': 1, 'message': '缺少记录ID'})
        
        # 验证记录是否存在且属于当前用户
        record = FoodRecord.query.filter_by(id=record_id, user_id=user_id).first()
        if not record:
            return jsonify({'code': 1, 'message': '记录不存在或无权限删除'})
        
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'code': 0, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'message': f'删除失败: {str(e)}'})

@record_bp.route('/getByDate', methods=['GET'])
def get_daily_record():
    """获取用户当日食物和热量记录"""
    try:
        # 在测试阶段固定使用ID为1的测试用户
        user_id = 1
        date_str = request.args.get('date')
        
        if not date_str:
            return jsonify({'code': 1, 'message': '缺少日期参数'})
        
        # 解析日期
        record_date = format_date(date_str)
        
        # 查询当日所有食物记录
        records = FoodRecord.query.filter_by(
            user_id=user_id, 
            record_date=record_date
        ).order_by(FoodRecord.record_time).all()
        
        # 按餐次分组
        meal_groups = {}
        for record in records:
            meal_type = get_meal_type_display(record.meal_type)
            # 格式化时间为HH:MM
            meal_time = record.record_time.strftime('%H:%M')
            
            if meal_type not in meal_groups:
                meal_groups[meal_type] = {
                    'mealType': meal_type,
                    'mealTime': meal_time,  # 使用第一条记录的时间
                    'foods': []
                }
            
            # 添加食物记录
            meal_groups[meal_type]['foods'].append({
                'recordId': record.id,
                'name': record.custom_food_name,
                'calories': float(record.calories),
                'protein': float(record.protein),
                'fat': float(record.fat),
                'carbs': float(record.carbs),
                'quantity': ''  # 暂无数量字段，可留空
            })
        
        # 转换为前端需要的格式
        food_records = list(meal_groups.values())
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': {
                'date': date_str,
                'foodRecords': food_records
            }
        })
    except Exception as e:
        return jsonify({'code': 1, 'message': f'获取食物记录失败: {str(e)}'})

@record_bp.route('/getNutrition', methods=['GET'])
def get_remaining():
    """获取用户当日剩余热量和营养记录"""
    try:
        # 在测试阶段固定使用ID为1的测试用户
        user_id = 1
        date_str = request.args.get('date')
        
        if not date_str:
            return jsonify({'code': 1, 'message': '缺少日期参数'})
        
        # 解析日期
        record_date = format_date(date_str)
        
        # 查询用户目标值
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        if profile:
            calorie_target = float(profile.calorie_target or 2000)
            protein_target = float(profile.protein_target or 125)
            fat_target = float(profile.fat_target or 83)
            carb_target = float(profile.carb_target or 313)
        else:
            # 如果没有设置目标，使用默认值
            calorie_target = 2000
            protein_target = 125
            fat_target = 83
            carb_target = 313
        
        # 查询当日已摄入营养素总和
        records = FoodRecord.query.filter_by(
            user_id=user_id,
            record_date=record_date
        ).all()
        
        current_calories = sum(float(record.calories or 0) for record in records)
        current_protein = sum(float(record.protein or 0) for record in records)
        current_fat = sum(float(record.fat or 0) for record in records)
        current_carbs = sum(float(record.carbs or 0) for record in records)
        
        # 计算百分比
        calories_percentage = min(int(current_calories / calorie_target * 100) if calorie_target > 0 else 0, 100)
        protein_percentage = min(int(current_protein / protein_target * 100) if protein_target > 0 else 0, 100)
        fat_percentage = min(int(current_fat / fat_target * 100) if fat_target > 0 else 0, 100)
        carbs_percentage = min(int(current_carbs / carb_target * 100) if carb_target > 0 else 0, 100)
        
        # 计算剩余热量
        remaining_calories = max(0, calorie_target - current_calories)
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': {
                'date': date_str,
                'nutritionData': {
                    'calories': {
                        'current': current_calories,
                        'target': calorie_target,
                        'percentage': calories_percentage,
                        'remaining': remaining_calories
                    },
                    'protein': {
                        'current': current_protein,
                        'target': protein_target,
                        'percentage': protein_percentage
                    },
                    'fat': {
                        'current': current_fat,
                        'target': fat_target,
                        'percentage': fat_percentage
                    },
                    'carbs': {
                        'current': current_carbs,
                        'target': carb_target,
                        'percentage': carbs_percentage
                    }
                }
            }
        })
    except Exception as e:
        return jsonify({'code': 1, 'message': f'获取营养摄入数据失败: {str(e)}'})

@record_bp.route('/getRecordDates', methods=['GET'])
def get_record_dates():
    """获取某月有记录的日期"""
    try:
        # 在测试阶段固定使用ID为1的测试用户
        user_id = 1
        year = request.args.get('year')
        month = request.args.get('month')
        
        if not year or not month:
            return jsonify({'code': 1, 'message': '缺少年份或月份参数'})
        
        year = int(year)
        month = int(month)
        
        # 获取当月第一天和最后一天
        first_day = datetime.date(year, month, 1)
        if month == 12:
            last_day = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        
        # 查询当月有记录的日期
        from sqlalchemy import func
        record_dates_query = db.session.query(
            func.extract('day', FoodRecord.record_date).label('day')
        ).filter(
            FoodRecord.user_id == user_id,
            FoodRecord.record_date.between(first_day, last_day)
        ).distinct().all()
        
        record_dates = [int(result[0]) for result in record_dates_query]
        
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': {
                'year': year,
                'month': month,
                'recordDates': record_dates
            }
        })
    except Exception as e:
        return jsonify({'code': 1, 'message': f'获取记录日期失败: {str(e)}'}) 
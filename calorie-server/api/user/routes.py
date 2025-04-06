from flask import Blueprint, request, jsonify
from ..services.nutrition_calculator import (
    calculate_bmr, calculate_tdee, calculate_macros, calculate_calorie_deficit
)
from ..models import db
from ..models.user import User, UserProfile
import requests
import json
import os
from datetime import datetime, timedelta
import jwt

user_bp = Blueprint('user', __name__)

# 微信小程序配置
APPID = "wx150476c0c0576c07"  # 从环境变量获取，或直接填写
SECRET = "11a935016aa6f577089b810a5dca539d"  # 从环境变量获取，或直接填写

@user_bp.route('/calculateBMR', methods=['POST'])
def calculate_bmr_route():
    """计算基础代谢率"""
    data = request.get_json()
    
    # 验证输入数据
    required_fields = ['weight', 'height', 'age', 'gender']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必要的参数'}), 400
    
    try:
        # 调用计算服务
        bmr = calculate_bmr(
            weight=float(data['weight']),
            height=float(data['height']),
            age=int(data['age']),
            gender=data['gender']
        )
        
        # 如果提供了用户ID，保存数据到数据库
        user_id = data.get('user_id')
        if user_id:
            save_user_profile_data(user_id, {
                'height': float(data['height']),
                'weight': float(data['weight']),
                'age': int(data['age']),
                'gender': data['gender'],
                'bmr': bmr
            })
        
        return jsonify({
            'bmr': bmr,
            'message': '基础代谢率计算成功'
        })
    except Exception as e:
        return jsonify({'error': f'计算过程中出错: {str(e)}'}), 500

@user_bp.route('/calculateTDEE', methods=['POST'])
def calculate_tdee_route():
    """计算总能量消耗"""
    data = request.get_json()
    
    # 验证输入数据
    if 'bmr' not in data or 'activity_level' not in data:
        return jsonify({'error': '缺少必要的参数'}), 400
    
    try:
        # 调用计算服务
        tdee = calculate_tdee(
            bmr=float(data['bmr']),
            activity_level=data['activity_level']
        )
        
        # 如果提供了用户ID，保存数据到数据库
        user_id = data.get('user_id')
        if user_id:
            save_user_profile_data(user_id, {
                'activity_level': data['activity_level'],
                'tdee': tdee
            })
        
        return jsonify({
            'tdee': tdee,
            'message': '总能量消耗计算成功'
        })
    except Exception as e:
        return jsonify({'error': f'计算过程中出错: {str(e)}'}), 500

@user_bp.route('/calculateNutrients', methods=['POST'])
def calculate_nutrients_route():
    """计算蛋白质、脂肪、碳水化合物需求量"""
    data = request.get_json()
    
    # 验证输入数据
    if 'tdee' not in data:
        return jsonify({'error': '缺少必要的参数'}), 400
    
    goal = data.get('goal', 'maintain')  # 默认为维持体重
    
    try:
        # 调用计算服务
        macros = calculate_macros(
            tdee=float(data['tdee']),
            goal=goal
        )
        
        # 如果提供了用户ID，保存数据到数据库
        user_id = data.get('user_id')
        if user_id:
            save_user_profile_data(user_id, {
                'calorie_target': macros['calorie_target'],
                'protein_target': macros['protein'],
                'fat_target': macros['fat'],
                'carb_target': macros['carb']
            })
        
        return jsonify({
            'nutrients': macros,
            'message': '营养素需求量计算成功'
        })
    except Exception as e:
        return jsonify({'error': f'计算过程中出错: {str(e)}'}), 500

@user_bp.route('/calculateCalorie', methods=['POST'])
def calculate_calorie_route():
    """计算用户热量需求和热量缺口"""
    data = request.get_json()
    
    # 验证输入数据
    if 'tdee' not in data:
        return jsonify({'error': '缺少必要的参数'}), 400
    
    current_intake = data.get('current_intake', 0)  # 当前摄入热量，默认为0
    goal = data.get('goal', 'maintain')  # 默认为维持体重
    
    try:
        # 计算宏量营养素和热量目标
        macros = calculate_macros(
            tdee=float(data['tdee']),
            goal=goal
        )
        
        # 计算热量缺口
        deficit = calculate_calorie_deficit(
            tdee=float(data['tdee']),
            current_intake=float(current_intake)
        )
        
        # 如果提供了用户ID，保存数据到数据库
        user_id = data.get('user_id')
        if user_id:
            save_user_profile_data(user_id, {
                'calorie_target': macros['calorie_target']
            })
        
        return jsonify({
            'calorie_target': macros['calorie_target'],
            'calorie_deficit': deficit,
            'message': '热量需求和缺口计算成功'
        })
    except Exception as e:
        return jsonify({'error': f'计算过程中出错: {str(e)}'}), 500

@user_bp.route('/calculateAll', methods=['POST'])
def calculate_all_route():
    """一次性计算所有营养指标"""
    data = request.get_json()
    
    # 验证输入数据
    required_fields = ['weight', 'height', 'age', 'gender', 'activity_level']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必要的参数'}), 400
    
    goal = data.get('goal', 'maintain')  # 默认为维持体重
    current_intake = data.get('current_intake', 0)  # 当前摄入热量，默认为0
    
    try:
        # 计算BMR
        bmr = calculate_bmr(
            weight=float(data['weight']),
            height=float(data['height']),
            age=int(data['age']),
            gender=data['gender']
        )
        
        # 计算TDEE
        tdee = calculate_tdee(
            bmr=bmr,
            activity_level=data['activity_level']
        )
        
        # 计算宏量营养素
        macros = calculate_macros(
            tdee=tdee,
            goal=goal
        )
        
        # 计算热量缺口
        deficit = calculate_calorie_deficit(
            tdee=tdee,
            current_intake=float(current_intake)
        )
        
        # 如果用户已登录，保存这些计算结果
        user_id = data.get('user_id')
        if user_id:
            # 保存所有计算结果到用户档案
            profile_data = {
                'height': float(data['height']),
                'weight': float(data['weight']),
                'age': int(data['age']),
                'gender': data['gender'],
                'activity_level': data['activity_level'],
                'bmr': bmr,
                'tdee': tdee,
                'calorie_target': macros['calorie_target'],
                'protein_target': macros['protein'],
                'fat_target': macros['fat'],
                'carb_target': macros['carb']
            }
            save_user_profile_data(user_id, profile_data)
        
        return jsonify({
            'bmr': bmr,
            'tdee': tdee,
            'calorie_target': macros['calorie_target'],
            'protein': macros['protein'],
            'fat': macros['fat'],
            'carb': macros['carb'],
            'calorie_deficit': deficit,
            'message': '营养指标计算成功'
        })
    except Exception as e:
        return jsonify({'error': f'计算过程中出错: {str(e)}'}), 500

def save_user_profile_data(user_id, data):
    """
    保存用户档案数据到数据库
    
    参数:
    user_id (int): 用户ID
    data (dict): 要保存的数据字典
    """
    try:
        # 查找用户
        user = User.query.get(user_id)
        if not user:
            print(f"用户ID {user_id} 不存在")
            return False
        
        # 查找或创建用户档案
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.session.add(profile)
        
        # 更新档案数据
        for key, value in data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        # 提交更改
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"保存用户档案数据失败: {str(e)}")
        return False

@user_bp.route('/info', methods=['GET', 'PUT'])
def user_info():
    """获取和更新用户基本信息"""
    # 从请求头中获取token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        # 解码token
        payload = jwt.decode(token, os.environ.get('SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
        user_id = payload.get('user_id')
        
        if request.method == 'GET':
            # 获取用户信息
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': '用户不存在'}), 404
            
            # 获取用户档案
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            
            # 构建响应数据
            user_data = {
                'id': user.id,
                'openid': user.openid,
                'nickname': user.nickname,
                'avatar_url': user.avatar_url
            }
            
            if profile:
                user_data.update({
                    'height': profile.height,
                    'weight': profile.weight,
                    'age': profile.age,
                    'gender': profile.gender,
                    'activity_level': profile.activity_level,
                    'bmr': profile.bmr,
                    'tdee': profile.tdee,
                    'calorie_target': profile.calorie_target,
                    'protein_target': profile.protein_target,
                    'fat_target': profile.fat_target,
                    'carb_target': profile.carb_target
                })
            
            return jsonify({
                'user': user_data,
                'message': '获取用户信息成功'
            })
        else:  # PUT
            data = request.get_json()
            
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': '用户不存在'}), 404
            
            # 更新用户基本信息
            if 'nickname' in data:
                user.nickname = data['nickname']
            if 'avatar_url' in data:
                user.avatar_url = data['avatar_url']
            
            # 更新用户档案信息
            profile_fields = ['height', 'weight', 'age', 'gender', 'activity_level']
            profile_data = {k: v for k, v in data.items() if k in profile_fields and v is not None}
            
            if profile_data:
                save_user_profile_data(user_id, profile_data)
            
            # 提交用户基本信息更改
            db.session.commit()
            
            return jsonify({
                'message': '更新用户信息成功'
            })
    
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'操作失败: {str(e)}'}), 500

@user_bp.route('/settings', methods=['GET', 'PUT'])
def user_settings():
    """管理用户设置"""
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': '缺少用户ID参数'}), 400
        
        try:
            # 获取用户档案中的设置信息
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                return jsonify({'error': '用户档案不存在'}), 404
            
            settings = {
                'calorie_target': profile.calorie_target,
                'protein_target': profile.protein_target,
                'fat_target': profile.fat_target,
                'carb_target': profile.carb_target
            }
            
            return jsonify({
                'settings': settings,
                'message': '获取用户设置成功'
            })
        except Exception as e:
            return jsonify({'error': f'获取用户设置失败: {str(e)}'}), 500
    else:  # PUT
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': '缺少用户ID参数'}), 400
        
        try:
            # 更新用户营养目标设置
            settings_fields = ['calorie_target', 'protein_target', 'fat_target', 'carb_target']
            settings_data = {k: v for k, v in data.items() if k in settings_fields and v is not None}
            
            if settings_data:
                save_user_profile_data(user_id, settings_data)
                return jsonify({'message': '更新用户设置成功'})
            else:
                return jsonify({'error': '没有提供有效的设置数据'}), 400
        except Exception as e:
            return jsonify({'error': f'更新用户设置失败: {str(e)}'}), 500

@user_bp.route('/feedback', methods=['POST'])
def user_feedback():
    """提交用户反馈"""
    data = request.get_json()
    
    # 验证输入数据
    required_fields = ['user_id', 'feedback_type', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必要的参数'}), 400
    
    try:
        from ..models.user import UserFeedback
        
        # 创建反馈记录
        feedback = UserFeedback(
            user_id=data['user_id'],
            feedback_type=data['feedback_type'],
            content=data['content'],
            contact_info=data.get('contact_info', '')
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'message': '反馈提交成功',
            'feedback_id': feedback.id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'提交反馈失败: {str(e)}'}), 500

@user_bp.route('/logout', methods=['POST'])
def user_logout():
    """用户退出登录"""
    # 由于使用的是JWT认证，客户端只需要删除本地存储的token即可
    return jsonify({'message': '退出登录成功'})

@user_bp.route('/login', methods=['POST'])
def login():
    print("收到登录请求")
    data = request.get_json()
    print(f"请求数据: {data}")
    
    code = data.get('code')
    if not code:
        print("缺少code参数")
        return jsonify({'error': 'Missing code parameter'}), 400
    
    print(f"获取到code: {code}")
    
    # 请求微信API获取openid和session_key
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={code}&grant_type=authorization_code'
    print(f"请求微信API: {url}")
    
    try:
        response = requests.get(url)
        wx_data = response.json()
        print(f"微信API返回: {wx_data}")
        
        # 检查微信返回的数据
        if 'errcode' in wx_data and wx_data['errcode'] != 0:
            error_msg = f"WeChat API error: {wx_data.get('errmsg', 'Unknown error')}, code: {wx_data.get('errcode', 'Unknown code')}"
            print(error_msg)
            return jsonify({'error': error_msg}), 400
        
        openid = wx_data.get('openid')
        session_key = wx_data.get('session_key')
        
        if not openid:
            print("未能从微信API获取openid")
            return jsonify({'error': 'Failed to get openid from WeChat API'}), 400
        
        print(f"获取到openid: {openid}")
        
        # 查找或创建用户
        user = User.query.filter_by(openid=openid).first()
        
        if not user:
            # 创建新用户
            user = User(openid=openid)
            db.session.add(user)
            db.session.commit()
            print(f"创建新用户，ID: {user.id}")
        else:
            print(f"找到现有用户，ID: {user.id}")
        
        # 更新用户的session_key
        user.session_key = session_key
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # 生成JWT token
        token_payload = {
            'user_id': user.id,
            'openid': openid,
            'exp': datetime.utcnow() + timedelta(days=30)  # 设置token过期时间
        }
        token = jwt.encode(token_payload, os.environ.get('SECRET_KEY', 'your-secret-key'), algorithm='HS256')
        print(f"生成token成功")
        
        # 获取用户资料
        profile = UserProfile.query.filter_by(user_id=user.id).first()
        user_info = {
            'id': user.id,
            'openid': openid,
            'nickname': user.nickname,
            'avatar_url': user.avatar_url
        }
        
        if profile:
            user_info.update({
                'height': profile.height,
                'weight': profile.weight,
                'age': profile.age,
                'gender': profile.gender,
                'activity_level': profile.activity_level,
                'calorie_target': profile.calorie_target,
                'protein_target': profile.protein_target,
                'fat_target': profile.fat_target,
                'carb_target': profile.carb_target
            })
        
        print(f"返回用户信息: {user_info}")
        return jsonify({
            'token': token,
            'userInfo': user_info
        })
    
    except Exception as e:
        error_msg = f"登录过程中出错: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return jsonify({'error': error_msg}), 500

@user_bp.route('/userinfo', methods=['GET'])
def get_user_info():
    # 从请求头中获取token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        # 解码token
        payload = jwt.decode(token, os.environ.get('SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
        user_id = payload.get('user_id')
        
        # 获取用户信息
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # 获取用户档案
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        # 构建响应数据
        user_data = {
            'id': user.id,
            'openid': user.openid,
            'nickname': user.nickname,
            'avatar_url': user.avatar_url,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
        
        if profile:
            user_data.update({
                'height': profile.height,
                'weight': profile.weight,
                'age': profile.age,
                'gender': profile.gender,
                'activity_level': profile.activity_level,
                'bmr': profile.bmr,
                'tdee': profile.tdee,
                'calorie_target': profile.calorie_target,
                'protein_target': profile.protein_target,
                'fat_target': profile.fat_target,
                'carb_target': profile.carb_target
            })
        
        return jsonify({
            'user': user_data,
            'message': '获取用户信息成功'
        })
    
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
from flask import Blueprint, request, jsonify
from models import db
from models.admin import Admin
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)

# 安全码，实际应用中应该存储在环境变量或配置文件中
SECURITY_CODE = 'ADMIN2023'

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': '请提供用户名和密码'}), 400
    
    admin = Admin.query.filter_by(username=data.get('username')).first()
    
    if not admin or not admin.check_password(data.get('password')):
        return jsonify({'message': '用户名或密码错误'}), 401
    
    # 更新最后登录时间
    admin.last_login = datetime.datetime.utcnow()
    db.session.commit()
    
    # 生成JWT令牌
    token = jwt.encode({
        'admin_id': admin.id,
        'username': admin.username,
        'role': admin.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, os.environ.get('SECRET_KEY', 'dev_secret_key'), algorithm='HS256')
    
    return jsonify({
        'token': token,
        'username': admin.username,
        'role': admin.role
    })

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': '无效的请求数据'}), 400
    
    # 验证必要字段
    required_fields = ['username', 'password', 'securityCode']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'缺少必要字段: {field}'}), 400
    
    # 验证安全码
    if data.get('securityCode') != SECURITY_CODE:
        return jsonify({'message': '安全码错误'}), 403
    
    # 检查用户名是否已存在
    existing_admin = Admin.query.filter_by(username=data.get('username')).first()
    if existing_admin:
        return jsonify({'message': '用户名已存在'}), 409
    
    # 创建新管理员
    new_admin = Admin(
        username=data.get('username'),
        password=data.get('password'),
        role='admin'  # 默认角色
    )
    
    db.session.add(new_admin)
    
    try:
        db.session.commit()
        return jsonify({'message': '注册成功', 'username': new_admin.username}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'注册失败: {str(e)}'}), 500 
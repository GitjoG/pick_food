from functools import wraps
from flask import request, jsonify
import jwt
import os
from models.admin import Admin

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头中获取token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': '缺少认证令牌'}), 401
        
        try:
            # 解码token
            data = jwt.decode(token, os.environ.get('SECRET_KEY', 'dev_secret_key'), algorithms=['HS256'])
            current_admin = Admin.query.filter_by(id=data['admin_id']).first()
            
            if not current_admin:
                return jsonify({'message': '无效的认证令牌'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '认证令牌已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '无效的认证令牌'}), 401
        
        # 将当前管理员传递给被装饰的函数
        return f(current_admin, *args, **kwargs)
    
    return decorated

def super_admin_required(f):
    @wraps(f)
    def decorated(current_admin, *args, **kwargs):
        if current_admin.role != 'super_admin':
            return jsonify({'message': '需要超级管理员权限'}), 403
        return f(current_admin, *args, **kwargs)
    
    return decorated 
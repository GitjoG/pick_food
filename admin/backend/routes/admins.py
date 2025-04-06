from flask import Blueprint, jsonify, request
from models import db
from models.admin import Admin
from middleware.admin_auth import admin_token_required, super_admin_required

admins_bp = Blueprint('admins', __name__)

@admins_bp.route('/profile', methods=['GET'])
@admin_token_required
def get_profile(current_admin):
    """获取当前管理员的个人资料"""
    return jsonify(current_admin.to_dict())

@admins_bp.route('/profile', methods=['PUT'])
@admin_token_required
def update_profile(current_admin):
    """更新当前管理员的个人资料"""
    data = request.get_json()
    
    if 'username' in data and data['username'] != current_admin.username:
        # 检查新用户名是否已存在
        existing_admin = Admin.query.filter_by(username=data['username']).first()
        if existing_admin:
            return jsonify({'message': '用户名已存在'}), 409
        current_admin.username = data['username']
    
    if 'password' in data:
        current_admin.set_password(data['password'])
    
    try:
        db.session.commit()
        return jsonify({'message': '个人资料更新成功', 'admin': current_admin.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'更新失败: {str(e)}'}), 500

@admins_bp.route('/list', methods=['GET'])
@admin_token_required
@super_admin_required
def get_admins(current_admin):
    """获取管理员列表（仅超级管理员可访问）"""
    admins = Admin.query.all()
    return jsonify([admin.to_dict() for admin in admins])

@admins_bp.route('/<int:admin_id>', methods=['GET'])
@admin_token_required
@super_admin_required
def get_admin(current_admin, admin_id):
    """获取特定管理员信息（仅超级管理员可访问）"""
    admin = Admin.query.get_or_404(admin_id)
    return jsonify(admin.to_dict())

@admins_bp.route('/<int:admin_id>', methods=['PUT'])
@admin_token_required
@super_admin_required
def update_admin(current_admin, admin_id):
    """更新特定管理员信息（仅超级管理员可访问）"""
    admin = Admin.query.get_or_404(admin_id)
    data = request.get_json()
    
    if 'username' in data and data['username'] != admin.username:
        existing_admin = Admin.query.filter_by(username=data['username']).first()
        if existing_admin:
            return jsonify({'message': '用户名已存在'}), 409
        admin.username = data['username']
    
    if 'password' in data:
        admin.set_password(data['password'])
    
    if 'role' in data:
        admin.role = data['role']
    
    try:
        db.session.commit()
        return jsonify({'message': '管理员更新成功', 'admin': admin.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'更新失败: {str(e)}'}), 500

@admins_bp.route('/<int:admin_id>', methods=['DELETE'])
@admin_token_required
@super_admin_required
def delete_admin(current_admin, admin_id):
    """删除特定管理员（仅超级管理员可访问）"""
    if current_admin.id == admin_id:
        return jsonify({'message': '不能删除当前登录的管理员'}), 403
    
    admin = Admin.query.get_or_404(admin_id)
    
    try:
        db.session.delete(admin)
        db.session.commit()
        return jsonify({'message': '管理员删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'删除失败: {str(e)}'}), 500 
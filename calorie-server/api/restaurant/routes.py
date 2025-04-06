from flask import Blueprint, request, jsonify

restaurant_bp = Blueprint('restaurant', __name__)

@restaurant_bp.route('/list', methods=['GET'])
def restaurant_list():
    """获取支持的餐厅列表"""
    # TODO: 实现获取餐厅列表的逻辑
    return jsonify({'message': '获取餐厅列表功能待实现'})

@restaurant_bp.route('/menu', methods=['GET'])
def restaurant_menu():
    """获取指定餐厅的菜单信息"""
    restaurant_id = request.args.get('restaurant_id')
    # TODO: 实现获取餐厅菜单的逻辑
    return jsonify({'message': f'获取餐厅{restaurant_id}菜单功能待实现'}) 
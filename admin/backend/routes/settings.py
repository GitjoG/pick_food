from flask import Blueprint, jsonify, request
from models import db
from models.settings import NutritionParameter, SystemNotification, UserFeedback
from models.user import User
from sqlalchemy import desc
from datetime import datetime

settings_bp = Blueprint('settings', __name__)

# 营养计算参数配置
@settings_bp.route('/settings/nutrition-params', methods=['GET'])
def get_nutrition_params():
    params = NutritionParameter.query.all()
    return jsonify([param.to_dict() for param in params])

# 系统通知管理
@settings_bp.route('/settings/notifications/list', methods=['GET'])
def get_notifications_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    is_active = request.args.get('is_active')
    
    query = SystemNotification.query
    
    if is_active is not None:
        is_active = is_active.lower() == 'true'
        query = query.filter(SystemNotification.is_active == is_active)
    
    pagination = query.order_by(desc(SystemNotification.created_at)).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
        'items': [notification.to_dict() for notification in pagination.items]
    })

@settings_bp.route('/settings/notifications/create', methods=['POST'])
def create_notification():
    data = request.json
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': '通知标题和内容不能为空'}), 400
    
    notification = SystemNotification(
        title=data['title'],
        content=data['content'],
        notification_type=data.get('notification_type', 'info'),
        is_active=data.get('is_active', True),
        start_time=datetime.fromisoformat(data['start_time']) if 'start_time' in data and data['start_time'] else None,
        end_time=datetime.fromisoformat(data['end_time']) if 'end_time' in data and data['end_time'] else None
    )
    
    db.session.add(notification)
    db.session.commit()
    
    return jsonify(notification.to_dict()), 201

@settings_bp.route('/settings/notifications/<int:notification_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_notification(notification_id):
    notification = SystemNotification.query.get_or_404(notification_id)
    
    if request.method == 'GET':
        return jsonify(notification.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        
        if not data:
            return jsonify({'error': '数据不能为空'}), 400
        
        if 'title' in data:
            notification.title = data['title']
        if 'content' in data:
            notification.content = data['content']
        if 'notification_type' in data:
            notification.notification_type = data['notification_type']
        if 'is_active' in data:
            notification.is_active = data['is_active']
        if 'start_time' in data:
            notification.start_time = datetime.fromisoformat(data['start_time']) if data['start_time'] else None
        if 'end_time' in data:
            notification.end_time = datetime.fromisoformat(data['end_time']) if data['end_time'] else None
        
        db.session.commit()
        
        return jsonify(notification.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({'message': '通知删除成功'})

# 用户反馈处理
@settings_bp.route('/settings/feedback/list', methods=['GET'])
def get_feedback_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    feedback_type = request.args.get('feedback_type')
    
    query = UserFeedback.query
    
    if status:
        query = query.filter(UserFeedback.status == status)
    
    if feedback_type:
        query = query.filter(UserFeedback.feedback_type == feedback_type)
    
    pagination = query.order_by(desc(UserFeedback.created_at)).paginate(page=page, per_page=per_page)
    
    feedbacks = []
    for feedback in pagination.items:
        feedback_dict = feedback.to_dict()
        user = User.query.get(feedback.user_id)
        feedback_dict['user_name'] = user.username if user else f"用户{feedback.user_id}"
        feedbacks.append(feedback_dict)
    
    return jsonify({
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
        'items': feedbacks
    })

@settings_bp.route('/settings/feedback/<int:feedback_id>', methods=['GET'])
def get_feedback_detail(feedback_id):
    feedback = UserFeedback.query.get_or_404(feedback_id)
    
    feedback_dict = feedback.to_dict()
    user = User.query.get(feedback.user_id)
    feedback_dict['user_name'] = user.username if user else f"用户{feedback.user_id}"
    
    return jsonify(feedback_dict)

@settings_bp.route('/settings/feedback/<int:feedback_id>/respond', methods=['POST'])
def respond_to_feedback(feedback_id):
    feedback = UserFeedback.query.get_or_404(feedback_id)
    
    data = request.json
    
    if not data or 'admin_response' not in data:
        return jsonify({'error': '回复内容不能为空'}), 400
    
    feedback.admin_response = data['admin_response']
    
    if 'status' in data:
        feedback.status = data['status']
    else:
        feedback.status = 'resolved'
    
    db.session.commit()
    
    return jsonify({
        'message': '反馈回复成功',
        'feedback': feedback.to_dict()
    }) 
from flask import Blueprint

def create_api_blueprint():
    """创建API蓝图"""
    api_bp = Blueprint('api', __name__)
    
    # 导入并注册各模块路由
    from .user.routes import user_bp
    from .restaurant.routes import restaurant_bp
    from .recommendation.routes import recommendation_bp
    from .record.routes import record_bp
    
    api_bp.register_blueprint(user_bp, url_prefix='/user')
    api_bp.register_blueprint(restaurant_bp, url_prefix='/restaurant')
    api_bp.register_blueprint(recommendation_bp, url_prefix='/recommendation')
    api_bp.register_blueprint(record_bp, url_prefix='/record')
    
    return api_bp 
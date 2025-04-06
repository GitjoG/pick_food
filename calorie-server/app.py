from flask import Flask
from flask_cors import CORS
from api import create_api_blueprint
from api.models import db
from config import config
from api.user.routes import user_bp

def create_app(config_name='default'):
    """创建Flask应用实例"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化CORS
    CORS(app)
    
    # 注册蓝图
    api_blueprint = create_api_blueprint()
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    # 导入所有模型以确保它们被正确注册
    with app.app_context():
        from api.models.user import User, UserProfile, UserFeedback
        from api.models.restaurant import Restaurant
        from api.models.food import FoodItem
        from api.models.record import FoodRecord
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=4000, debug=True) 
from flask import Blueprint
from .users import users_bp
from .restaurants import restaurants_bp
from .recommendation import recommendation_bp
from .statistics import statistics_bp
from .settings import settings_bp

def register_routes(app):
    # 添加调试日志
    print("Registering routes...")
    
    app.register_blueprint(users_bp, url_prefix='/admin/api')
    app.register_blueprint(restaurants_bp, url_prefix='/admin/api')
    app.register_blueprint(recommendation_bp, url_prefix='/admin/api')
    app.register_blueprint(statistics_bp, url_prefix='/admin/api')
    app.register_blueprint(settings_bp, url_prefix='/admin/api')
    
    # 注册后打印应用的路由
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule}") 
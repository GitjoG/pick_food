from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from models import db, init_db

from routes.restaurants import restaurants_bp
from routes.auth import auth_bp
from routes.users import users_bp
from routes.admins import admins_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# 初始化数据库
init_db(app)

# 注册蓝图
app.register_blueprint(restaurants_bp, url_prefix='/admin/api')
app.register_blueprint(auth_bp, url_prefix='/admin/api/auth')
app.register_blueprint(users_bp, url_prefix='/admin/api/users')
app.register_blueprint(admins_bp, url_prefix='/admin/api/admins')

# 添加调试路由信息
@app.before_request
def log_request_info():
    print('Request Path:', request.path)
    print('Request Method:', request.method)
    print('Request Args:', request.args)

# 添加路由列表端点
@app.route('/admin/api/routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'path': str(rule)
        })
    return jsonify(routes)

@app.route('/admin/api/health')
def health_check():
    return jsonify({"status": "ok", "message": "服务正常运行"})

def create_app():
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 
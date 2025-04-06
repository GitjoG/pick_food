from flask_migrate import Migrate
from app import create_app
from api.models import db

app = create_app('development')

# 初始化数据库迁移
migrate = Migrate(app, db)

# 在应用上下文中初始化数据库
with app.app_context():
    # 导入所有模型
    from api.models.user import User, UserProfile, UserFeedback
    from api.models.restaurant import Restaurant
    from api.models.food import FoodItem
    from api.models.record import FoodRecord
    
    # 创建所有表
    db.create_all()
    print("数据库表已创建")

if __name__ == '__main__':
    # 可以在这里添加一些初始数据
    with app.app_context():
        # 检查是否已有数据
        if User.query.count() == 0:
            print("添加初始测试数据...")
            # 添加测试数据的代码
            # ... 
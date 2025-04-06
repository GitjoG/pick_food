# 数据模型初始化
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 确保在导入模型之前先初始化db
# 这样可以避免循环导入问题 
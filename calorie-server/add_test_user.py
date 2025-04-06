from app import create_app
from api.models import db
from api.models.user import User

app = create_app('development')

with app.app_context():
    # 检查是否已有测试用户
    test_user = User.query.filter_by(openid='test_openid').first()
    
    if not test_user:
        # 创建测试用户
        test_user = User(
            openid='test_openid',
            nickname='测试用户',
            avatar_url='https://example.com/avatar.png'
        )
        db.session.add(test_user)
        db.session.commit()
        
        # 创建用户档案
        from api.models.user import UserProfile
        profile = UserProfile(
            user_id=test_user.id,
            height=175.0,
            weight=70.0,
            age=30,
            gender='male',
            activity_level='moderate',
            bmr=1700.0,
            tdee=2500.0,
            calorie_target=2000.0,
            protein_target=125.0,
            fat_target=83.0,
            carb_target=313.0
        )
        db.session.add(profile)
        db.session.commit()
        
        print(f"创建测试用户成功，ID: {test_user.id}")
    else:
        print(f"测试用户已存在，ID: {test_user.id}") 
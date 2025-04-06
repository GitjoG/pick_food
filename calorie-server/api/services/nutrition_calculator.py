"""
营养计算服务
包含计算BMR、TDEE、营养素需求等功能
"""

def calculate_bmr(weight, height, age, gender):
    """
    计算基础代谢率(BMR)
    使用Mifflin-St Jeor公式
    
    参数:
    weight (float): 体重(kg)
    height (float): 身高(cm)
    age (int): 年龄
    gender (str): 性别 ('male' 或 'female')
    
    返回:
    float: 基础代谢率(kcal/day)
    """
    if gender == 'male':
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:  # female
        return (10 * weight) + (6.25 * height) - (5 * age) - 161

def calculate_tdee(bmr, activity_level):
    """
    计算总能量消耗(TDEE)
    
    参数:
    bmr (float): 基础代谢率
    activity_level (str): 活动水平
    
    返回:
    float: 总能量消耗(kcal/day)
    """
    activity_multipliers = {
        'sedentary': 1.2,       # 久坐不动
        'light': 1.375,         # 轻度活动(每周运动1-3次)
        'moderate': 1.55,       # 中度活动(每周运动3-5次)
        'active': 1.725,        # 积极活动(每周运动6-7次)
        'very_active': 1.9      # 非常活跃(每天运动或体力劳动)
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.2)
    return bmr * multiplier

def calculate_macros(tdee, goal='maintain'):
    """
    计算宏量营养素需求
    
    参数:
    tdee (float): 总能量消耗
    goal (str): 目标 ('lose', 'maintain', 'gain')
    
    返回:
    dict: 包含蛋白质、脂肪、碳水化合物需求量的字典
    """
    # 根据目标调整热量
    if goal == 'lose':
        calorie_target = tdee * 0.8  # 减少20%热量
    elif goal == 'gain':
        calorie_target = tdee * 1.1  # 增加10%热量
    else:  # maintain
        calorie_target = tdee
    
    # 计算宏量营养素(按照标准比例)
    protein_g = 2.0 * (calorie_target * 0.3 / 4)  # 30%热量来自蛋白质，每克4卡路里
    fat_g = calorie_target * 0.25 / 9  # 25%热量来自脂肪，每克9卡路里
    carb_g = calorie_target * 0.45 / 4  # 45%热量来自碳水，每克4卡路里
    
    return {
        'calorie_target': round(calorie_target, 2),
        'protein': round(protein_g, 2),
        'fat': round(fat_g, 2),
        'carb': round(carb_g, 2)
    }

def calculate_calorie_deficit(tdee, current_intake):
    """
    计算热量缺口
    
    参数:
    tdee (float): 总能量消耗
    current_intake (float): 当前热量摄入
    
    返回:
    float: 热量缺口(负值表示摄入不足，正值表示摄入过多)
    """
    return current_intake - tdee 
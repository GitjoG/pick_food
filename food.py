import numpy as np
from typing import List, Dict, Tuple
import pandas as pd
from itertools import combinations

class FoodMatcher:
    def __init__(self, food_data: List[Dict]):
        """
        初始化食物匹配器
        
        Args:
            food_data: 包含食物信息的列表，每个食物是一个字典，包含名称、热量、碳水、蛋白质和脂肪
        """
        self.food_data = food_data
        # 将食物数据转换为DataFrame以便于处理
        self.food_df = pd.DataFrame(food_data)
    
    def match_foods(self, target_carbs: float, target_protein: float, target_fat: float, 
                   max_items: int = 5, tolerance: float = 0.1) -> List[Dict]:
        """
        根据目标营养需求匹配食物组合
        
        Args:
            target_carbs: 目标碳水化合物(克)
            target_protein: 目标蛋白质(克)
            target_fat: 目标脂肪(克)
            max_items: 最多选择的食物数量
            tolerance: 允许的误差范围(百分比)
            
        Returns:
            最佳匹配的食物组合列表
        """
        target = np.array([target_carbs, target_protein, target_fat])
        best_combination = None
        best_error = float('inf')
        
        # 尝试不同数量的食物组合
        for num_items in range(1, min(max_items + 1, len(self.food_data) + 1)):
            for combo_indices in combinations(range(len(self.food_data)), num_items):
                combo = [self.food_data[i] for i in combo_indices]
                
                # 计算当前组合的总营养成分
                total_carbs = sum(food['carbs'] for food in combo)
                total_protein = sum(food['protein'] for food in combo)
                total_fat = sum(food['fat'] for food in combo)
                current = np.array([total_carbs, total_protein, total_fat])
                
                # 计算与目标的误差
                error = np.sum(np.abs(current - target) / target)
                
                # 如果误差在容忍范围内或比之前找到的最佳组合更好
                if error < best_error:
                    best_error = error
                    best_combination = combo
                
                # 如果误差在容忍范围内，可以提前返回
                if error <= tolerance:
                    return combo
        
        return best_combination if best_combination else []
    
    def find_all_combinations(self, target_carbs: float, target_protein: float, target_fat: float,
                             max_items: int = 5, max_results: int = 10, tolerance: float = 0.15) -> List[List[Dict]]:
        """
        查找所有满足条件的食物组合
        
        Args:
            target_carbs: 目标碳水化合物(克)
            target_protein: 目标蛋白质(克)
            target_fat: 目标脂肪(克)
            max_items: 每个组合最多包含的食物数量
            max_results: 最多返回的组合数量
            tolerance: 允许的误差范围(百分比)
            
        Returns:
            满足条件的食物组合列表
        """
        target = np.array([target_carbs, target_protein, target_fat])
        valid_combinations = []
        
        # 尝试不同数量的食物组合
        for num_items in range(1, min(max_items + 1, len(self.food_data) + 1)):
            for combo_indices in combinations(range(len(self.food_data)), num_items):
                combo = [self.food_data[i] for i in combo_indices]
                
                # 计算当前组合的总营养成分
                total_carbs = sum(food['carbs'] for food in combo)
                total_protein = sum(food['protein'] for food in combo)
                total_fat = sum(food['fat'] for food in combo)
                current = np.array([total_carbs, total_protein, total_fat])
                
                # 计算与目标的误差
                error = np.sum(np.abs(current - target) / target)
                
                # 如果误差在容忍范围内，添加到有效组合列表
                if error <= tolerance:
                    # 计算组合的总热量，用于排序
                    total_calories = sum(food['calories'] for food in combo)
                    valid_combinations.append({
                        'foods': combo,
                        'error': error,
                        'total_carbs': total_carbs,
                        'total_protein': total_protein,
                        'total_fat': total_fat,
                        'total_calories': total_calories
                    })
        
        # 按误差排序
        valid_combinations.sort(key=lambda x: x['error'])
        
        # 返回前max_results个组合
        return valid_combinations[:max_results]
    
    def find_diverse_combinations(self, target_carbs: float, target_protein: float, target_fat: float,
                                max_items: int = 5, max_results: int = 10, tolerance: float = 0.15) -> List[List[Dict]]:
        """
        查找多样化的食物组合，确保返回的组合彼此不同
        
        Args:
            target_carbs: 目标碳水化合物(克)
            target_protein: 目标蛋白质(克)
            target_fat: 目标脂肪(克)
            max_items: 每个组合最多包含的食物数量
            max_results: 最多返回的组合数量
            tolerance: 允许的误差范围(百分比)
            
        Returns:
            多样化的食物组合列表
        """
        # 首先获取所有满足条件的组合
        all_combinations = self.find_all_combinations(
            target_carbs, target_protein, target_fat, 
            max_items, max_results * 3, tolerance
        )
        
        if not all_combinations:
            return []
        
        # 选择多样化的组合
        diverse_combinations = [all_combinations[0]]  # 先添加最佳组合
        
        for combo in all_combinations[1:]:
            # 检查这个组合与已选组合的不同程度
            is_diverse = True
            for selected_combo in diverse_combinations:
                # 计算两个组合中食物的重叠程度
                selected_foods = {food['name'] for food in selected_combo['foods']}
                current_foods = {food['name'] for food in combo['foods']}
                overlap = len(selected_foods.intersection(current_foods))
                
                # 如果重叠度高，认为不够多样化
                if overlap >= min(len(selected_foods), len(current_foods)) * 0.7:
                    is_diverse = False
                    break
            
            if is_diverse:
                diverse_combinations.append(combo)
                
            # 如果已经收集了足够多的多样化组合，停止
            if len(diverse_combinations) >= max_results:
                break
        
        return diverse_combinations
    
    def suggest_portions(self, target_carbs: float, target_protein: float, target_fat: float,
                        max_items: int = 5) -> List[Dict]:
        """
        建议食物组合及其份量
        
        Args:
            target_carbs: 目标碳水化合物(克)
            target_protein: 目标蛋白质(克)
            target_fat: 目标脂肪(克)
            max_items: 最多选择的食物数量
            
        Returns:
            包含食物名称和建议份量的列表
        """
        # 使用线性规划求解最优食物组合
        from scipy.optimize import linprog
        
        # 提取营养矩阵
        A = self.food_df[['carbs', 'protein', 'fat']].values
        
        # 目标函数：最小化总食物量
        c = np.ones(len(self.food_df))
        
        # 约束条件：总营养量 >= 目标营养量
        b = np.array([target_carbs, target_protein, target_fat])
        
        # 求解线性规划问题
        result = linprog(-c, A_ub=-A, b_ub=-b, bounds=(0, None), method='highs')
        
        if not result.success:
            # 如果线性规划失败，回退到组合方法
            return self.match_foods(target_carbs, target_protein, target_fat, max_items)
        
        # 获取结果
        portions = result.x
        
        # 筛选出份量大于0的食物
        selected_foods = []
        for i, portion in enumerate(portions):
            if portion > 0.01:  # 忽略非常小的份量
                food = self.food_df.iloc[i].to_dict()
                food['portion'] = round(portion, 2)
                selected_foods.append(food)
        
        # 如果选择的食物太多，只保留最重要的几个
        if len(selected_foods) > max_items:
            selected_foods.sort(key=lambda x: x['portion'], reverse=True)
            selected_foods = selected_foods[:max_items]
            
        return selected_foods

def example_usage():
    """示例用法"""
    # 示例食物数据
    foods = [
        {"name": "鸡胸肉", "calories": 165, "carbs": 0, "protein": 31, "fat": 3.6},
        {"name": "米饭", "calories": 130, "carbs": 28, "protein": 2.7, "fat": 0.3},
        {"name": "鸡蛋", "calories": 155, "carbs": 1.1, "protein": 12.6, "fat": 10.6},
        {"name": "牛奶", "calories": 42, "carbs": 5, "protein": 3.4, "fat": 1},
        {"name": "燕麦片", "calories": 389, "carbs": 66, "protein": 17, "fat": 7},
        {"name": "花生酱", "calories": 588, "carbs": 20, "protein": 25, "fat": 50},
        {"name": "香蕉", "calories": 89, "carbs": 23, "protein": 1.1, "fat": 0.3},
        {"name": "三文鱼", "calories": 208, "carbs": 0, "protein": 20, "fat": 13},
        {"name": "牛肉", "calories": 250, "carbs": 0, "protein": 26, "fat": 17},
        {"name": "豆腐", "calories": 76, "carbs": 1.9, "protein": 8, "fat": 4.2},
    ]
    
    # 创建食物匹配器
    matcher = FoodMatcher(foods)
    
    # 用户目标营养素
    target_carbs = 100
    target_protein = 60
    target_fat = 30
    
    # 获取匹配的食物
    matched_foods = matcher.match_foods(target_carbs, target_protein, target_fat)
    print("匹配的食物组合:")
    total_carbs, total_protein, total_fat, total_calories = 0, 0, 0, 0
    for food in matched_foods:
        print(f"{food['name']}: 碳水={food['carbs']}g, 蛋白质={food['protein']}g, 脂肪={food['fat']}g, 热量={food['calories']}卡")
        total_carbs += food['carbs']
        total_protein += food['protein']
        total_fat += food['fat']
        total_calories += food['calories']
    
    print(f"\n总计: 碳水={total_carbs}g, 蛋白质={total_protein}g, 脂肪={total_fat}g, 热量={total_calories}卡")
    print(f"目标: 碳水={target_carbs}g, 蛋白质={target_protein}g, 脂肪={target_fat}g")
    
    # 获取多种食物组合
    print("\n多种食物组合方案:")
    diverse_combinations = matcher.find_diverse_combinations(target_carbs, target_protein, target_fat)
    
    for i, combo in enumerate(diverse_combinations):
        print(f"\n方案 {i+1} (误差: {combo['error']:.3f}):")
        for food in combo['foods']:
            print(f"{food['name']}: 碳水={food['carbs']}g, 蛋白质={food['protein']}g, 脂肪={food['fat']}g, 热量={food['calories']}卡")
        print(f"总计: 碳水={combo['total_carbs']}g, 蛋白质={combo['total_protein']}g, 脂肪={combo['total_fat']}g, 热量={combo['total_calories']}卡")

if __name__ == "__main__":
    example_usage()

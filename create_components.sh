#!/bin/bash

# 在 frontend/src/views 目录下运行这个脚本

# 推荐管理组件
mkdir -p recommendation
cat > recommendation/AlgorithmParams.vue << 'EOF'
<template>
  <div class="page-container">
    <h1>推荐算法参数配置</h1>
    <div class="page-content">
      <el-card>
        <div>功能开发中...</div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlgorithmParams'
}
</script>

<style scoped>
.page-container {
  padding: 20px;
}
.page-content {
  margin-top: 20px;
}
</style>
EOF

# 复制基础模板到其他组件
cp recommendation/AlgorithmParams.vue recommendation/RecommendationRules.vue
cp recommendation/AlgorithmParams.vue recommendation/RecommendationResults.vue

# 餐厅管理组件
mkdir -p restaurants
cp recommendation/AlgorithmParams.vue restaurants/RestaurantList.vue
cp recommendation/AlgorithmParams.vue restaurants/RestaurantDetail.vue
cp recommendation/AlgorithmParams.vue restaurants/RestaurantMenu.vue

# 设置组件
mkdir -p settings
cp recommendation/AlgorithmParams.vue settings/NutritionParams.vue
cp recommendation/AlgorithmParams.vue settings/SystemNotifications.vue
cp recommendation/AlgorithmParams.vue settings/UserFeedbacks.vue

# 统计组件
mkdir -p statistics
cp recommendation/AlgorithmParams.vue statistics/NutritionGoalsStats.vue
cp recommendation/AlgorithmParams.vue statistics/PopularFoodsStats.vue
cp recommendation/AlgorithmParams.vue statistics/UserPreferencesStats.vue

# 用户管理组件
mkdir -p users
cp recommendation/AlgorithmParams.vue users/UserDetail.vue
cp recommendation/AlgorithmParams.vue users/UserNutritionGoals.vue
cp recommendation/AlgorithmParams.vue users/UserCalorieRecords.vue
cp recommendation/AlgorithmParams.vue users/UserPreferences.vue 
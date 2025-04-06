<template>
  <div class="page-container">
    <h1>用户详情</h1>
    <el-card class="user-info">
      <el-form label-width="100px">
        <el-form-item label="用户名">
          <span>{{ userInfo.username }}</span>
        </el-form-item>
        <el-form-item label="手机号">
          <span>{{ userInfo.phone }}</span>
        </el-form-item>
        <el-form-item label="注册时间">
          <span>{{ userInfo.created_at }}</span>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-tabs v-model="activeTab" class="user-tabs">
      <el-tab-pane label="营养目标" name="nutrition">
        <nutrition-goals :user-id="userId" />
      </el-tab-pane>
      <el-tab-pane label="热量记录" name="calories">
        <calorie-records :user-id="userId" />
      </el-tab-pane>
      <el-tab-pane label="饮食偏好" name="preferences">
        <user-preferences :user-id="userId" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import NutritionGoals from './components/NutritionGoals'
import CalorieRecords from './components/CalorieRecords'
import UserPreferences from './components/UserPreferences'
import axios from 'axios'

export default {
  name: 'UserDetail',
  components: {
    NutritionGoals,
    CalorieRecords,
    UserPreferences
  },
  data() {
    return {
      userId: this.$route.params.id,
      userInfo: {},
      activeTab: 'nutrition'
    }
  },
  created() {
    this.fetchUserInfo()
  },
  methods: {
    async fetchUserInfo() {
      try {
        const response = await axios.get(`/users/${this.userId}`)
        this.userInfo = response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.$message.error('获取用户信息失败')
        
        // 使用模拟数据
        this.userInfo = {
          username: '测试用户',
          phone: '13800138000',
          created_at: '2023-01-01'
        }
      }
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 20px;
}
.user-info {
  margin-bottom: 20px;
}
.user-tabs {
  margin-top: 20px;
}
</style> 
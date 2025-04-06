<template>
  <div class="user-preferences">
    <el-card>
      <div slot="header">
        <span>饮食偏好</span>
      </div>
      <el-form label-width="120px">
        <el-form-item label="喜欢的食物">
          <el-tag v-for="(food, index) in preferences.likedFoods" :key="'like-'+index" type="success" style="margin-right: 5px">
            {{ food }}
          </el-tag>
        </el-form-item>
        <el-form-item label="不喜欢的食物">
          <el-tag v-for="(food, index) in preferences.dislikedFoods" :key="'dislike-'+index" type="danger" style="margin-right: 5px">
            {{ food }}
          </el-tag>
        </el-form-item>
        <el-form-item label="饮食限制">
          <el-tag v-for="(restriction, index) in preferences.dietaryRestrictions" :key="'restriction-'+index" type="info" style="margin-right: 5px">
            {{ restriction }}
          </el-tag>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'UserPreferences',
  props: {
    userId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      preferences: {
        likedFoods: ['鸡胸肉', '西兰花', '糙米'],
        dislikedFoods: ['茄子', '苦瓜'],
        dietaryRestrictions: ['低糖', '低盐']
      }
    }
  },
  created() {
    this.fetchUserPreferences()
  },
  methods: {
    fetchUserPreferences() {
      // 这里应该从API获取数据
      console.log('Fetching preferences for user:', this.userId)
    }
  }
}
</script> 
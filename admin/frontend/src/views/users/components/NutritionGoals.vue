<template>
  <div class="nutrition-goals">
    <el-card>
      <div slot="header">
        <span>营养目标</span>
      </div>
      <el-form label-width="120px">
        <el-form-item label="每日热量目标">
          <span>{{ goals.calories }} kcal</span>
        </el-form-item>
        <el-form-item label="蛋白质目标">
          <span>{{ goals.protein }} g</span>
        </el-form-item>
        <el-form-item label="脂肪目标">
          <span>{{ goals.fat }} g</span>
        </el-form-item>
        <el-form-item label="碳水目标">
          <span>{{ goals.carbs }} g</span>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'NutritionGoals',
  props: {
    userId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      goals: {
        calories: 2000,
        protein: 100,
        fat: 70,
        carbs: 250
      }
    }
  },
  created() {
    this.fetchNutritionGoals()
  },
  methods: {
    fetchNutritionGoals() {
      // 这里应该从API获取数据
      console.log('Fetching nutrition goals for user:', this.userId)
    }
  }
}
</script> 
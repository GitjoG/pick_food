<template>
  <div class="calorie-records">
    <el-card>
      <div slot="header">
        <span>热量记录</span>
      </div>
      <el-table :data="records" style="width: 100%">
        <el-table-column prop="date" label="日期"></el-table-column>
        <el-table-column prop="calories" label="热量 (kcal)"></el-table-column>
        <el-table-column prop="protein" label="蛋白质 (g)"></el-table-column>
        <el-table-column prop="fat" label="脂肪 (g)"></el-table-column>
        <el-table-column prop="carbs" label="碳水 (g)"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'CalorieRecords',
  props: {
    userId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      records: [
        {
          date: '2023-05-01',
          calories: 1850,
          protein: 95,
          fat: 65,
          carbs: 220
        },
        {
          date: '2023-05-02',
          calories: 1920,
          protein: 100,
          fat: 68,
          carbs: 230
        }
      ]
    }
  },
  created() {
    this.fetchCalorieRecords()
  },
  methods: {
    fetchCalorieRecords() {
      // 这里应该从API获取数据
      console.log('Fetching calorie records for user:', this.userId)
    }
  }
}
</script> 
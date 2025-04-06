<template>
  <div class="dashboard">
    <h1>仪表盘</h1>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <div slot="header">用户总数</div>
          <div class="card-content">0</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div slot="header">餐厅总数</div>
          <div class="card-content">0</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div slot="header">今日活跃用户</div>
          <div class="card-content">0</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div slot="header">待处理反馈</div>
          <div class="card-content">0</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
.card-content {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  padding: 20px 0;
}
</style> 
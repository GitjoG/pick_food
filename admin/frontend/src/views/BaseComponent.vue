<template>
  <div class="page-container">
    <h1>{{ title }}</h1>
    <div class="page-content">
      <!-- 页面内容将在这里实现 -->
      <el-card>
        <div>功能开发中...</div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseComponent',
  data() {
    return {
      title: '页面标题'
    }
  }
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
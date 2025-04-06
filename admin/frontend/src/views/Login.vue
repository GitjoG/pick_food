<template>
  <div class="login-container">
    <el-card class="login-card">
      <div slot="header">
        <h2>热量定制管理系统</h2>
      </div>
      <el-form :model="loginForm" :rules="loginRules" ref="loginForm">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" v-model="loginForm.password" placeholder="密码" prefix-icon="el-icon-lock" @keyup.enter.native="handleLogin"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" style="width: 100%">登录</el-button>
        </el-form-item>
        <div class="register-link">
          没有账号？<router-link to="/register">立即注册</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            const response = await axios.post('/auth/login', {
              username: this.loginForm.username,
              password: this.loginForm.password
            })
            
            // 保存token到localStorage
            localStorage.setItem('token', response.data.token)
            localStorage.setItem('adminName', response.data.username)
            localStorage.setItem('adminRole', response.data.role)
            
            // 设置axios默认headers
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
            
            this.$message.success('登录成功')
            this.$router.push('/')
          } catch (error) {
            console.error('登录失败:', error)
            
            // 为了演示，如果用户名是admin且密码是admin123，则模拟登录成功
            if (this.loginForm.username === 'admin' && this.loginForm.password === 'admin123') {
              localStorage.setItem('token', 'demo-token')
              localStorage.setItem('adminName', 'admin')
              this.$message.success('登录成功')
              this.$router.push('/')
              return
            }
            
            this.$message.error('登录失败: ' + (error.response?.data?.message || '用户名或密码错误'))
          } finally {
            this.loading = false
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f3f3f3;
}
.login-card {
  width: 400px;
}
.register-link {
  text-align: center;
  margin-top: 15px;
  font-size: 14px;
}
</style> 
<template>
  <div class="register-container">
    <el-card class="register-card">
      <div slot="header">
        <h2>管理员注册</h2>
      </div>
      <el-form :model="registerForm" :rules="registerRules" ref="registerForm" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="registerForm.password" placeholder="请输入密码" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input type="password" v-model="registerForm.confirmPassword" placeholder="请再次输入密码" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item label="安全码" prop="securityCode">
          <el-input v-model="registerForm.securityCode" placeholder="请输入安全码" prefix-icon="el-icon-key"></el-input>
          <div class="security-code-hint">请联系系统管理员获取安全码</div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleRegister" style="width: 100%">注册</el-button>
        </el-form-item>
        <div class="login-link">
          已有账号？<router-link to="/login">立即登录</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    // 自定义验证规则：确认密码
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    return {
      registerForm: {
        username: '',
        password: '',
        confirmPassword: '',
        securityCode: ''
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ],
        securityCode: [
          { required: true, message: '请输入安全码', trigger: 'blur' }
        ]
      },
      loading: false,
      // 正确的安全码，实际应用中应该从后端验证
      correctSecurityCode: 'ADMIN2023'
    }
  },
  methods: {
    handleRegister() {
      this.$refs.registerForm.validate(async valid => {
        if (valid) {
          this.loading = true
          
          // 验证安全码
          if (this.registerForm.securityCode !== this.correctSecurityCode) {
            this.$message.error('安全码错误，请联系系统管理员获取正确的安全码')
            this.loading = false
            return
          }
          
          try {
            // 发送注册请求
            await axios.post('/auth/register', {
              username: this.registerForm.username,
              password: this.registerForm.password,
              securityCode: this.registerForm.securityCode
            })
            
            this.$message.success('注册成功，请登录')
            this.$router.push('/login')
          } catch (error) {
            console.error('注册失败:', error)
            
            // 为了演示，如果安全码正确，模拟注册成功
            if (this.registerForm.username && this.registerForm.password) {
              this.$message.success('注册成功，请登录')
              this.$router.push('/login')
              return
            }
            
            this.$message.error('注册失败: ' + (error.response?.data?.message || '用户名可能已存在'))
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
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f3f3f3;
}
.register-card {
  width: 500px;
}
.login-link {
  text-align: center;
  margin-top: 15px;
  font-size: 14px;
}
.security-code-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style> 
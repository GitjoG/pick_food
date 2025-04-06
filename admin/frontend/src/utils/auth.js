import axios from 'axios'
import router from '@/router'
import { Message } from 'element-ui'

// 检查用户是否已登录
export function isLoggedIn() {
  return !!localStorage.getItem('token')
}

// 获取管理员名称
export function getAdminName() {
  return localStorage.getItem('adminName') || '管理员'
}

// 设置认证token
export function setToken(token) {
  localStorage.setItem('token', token)
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

// 清除认证信息
export function clearAuth() {
  localStorage.removeItem('token')
  localStorage.removeItem('adminName')
  delete axios.defaults.headers.common['Authorization']
}

// 登出
export function logout() {
  clearAuth()
  router.push('/login')
  Message.success('已退出登录')
}

// 初始化认证状态
export function initAuth() {
  const token = localStorage.getItem('token')
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
} 
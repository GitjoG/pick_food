const api = require('./api')

// 计算基础代谢率
const calculateBMR = (userData) => {
  return api.post('/api/user/calculateBMR', userData)
}

// 计算总能量消耗
const calculateTDEE = (userData) => {
  return api.post('/api/user/calculateTDEE', userData)
}

// 计算营养素需求
const calculateNutrients = (userData) => {
  return api.post('/api/user/calculateNutrients', userData)
}

// 计算热量需求和热量缺口
const calculateCalorie = (userData) => {
  return api.post('/api/user/calculateCalorie', userData)
}

// 获取用户当日营养摄入情况
const getDailyNutrition = () => {
  return api.get('/api/record/getDaily')
}

// 获取用户当日剩余热量和营养
const getRemainingNutrition = () => {
  return api.get('/api/record/getRemaining')
}

// 添加一次性计算所有营养指标的方法
const calculateAll = (userData) => {
  return api.post('/api/user/calculateAll', userData)
}

module.exports = {
  calculateBMR,
  calculateTDEE,
  calculateNutrients,
  calculateCalorie,
  getDailyNutrition,
  getRemainingNutrition,
  calculateAll
} 
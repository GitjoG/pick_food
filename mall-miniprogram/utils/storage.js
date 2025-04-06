// 存储用户信息
const saveUserInfo = (userInfo) => {
  wx.setStorageSync('userInfo', userInfo)
}

// 获取用户信息
const getUserInfo = () => {
  return wx.getStorageSync('userInfo') || null
}

// 存储营养目标
const saveNutritionGoals = (goals) => {
  wx.setStorageSync('nutritionGoals', goals)
}

// 获取营养目标
const getNutritionGoals = () => {
  return wx.getStorageSync('nutritionGoals') || null
}

// 存储食物记录
const saveFoodRecords = (records) => {
  wx.setStorageSync('foodRecords', records)
}

// 获取食物记录
const getFoodRecords = () => {
  return wx.getStorageSync('foodRecords') || []
}

// 清除所有存储
const clearStorage = () => {
  wx.clearStorageSync()
}

module.exports = {
  saveUserInfo,
  getUserInfo,
  saveNutritionGoals,
  getNutritionGoals,
  saveFoodRecords,
  getFoodRecords,
  clearStorage
} 
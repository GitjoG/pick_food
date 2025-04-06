const api = require('./api')

// 添加食物记录
const addFoodRecord = (recordData) => {
  return api.post('api/record/add', recordData)
}

// 更新食物记录
const updateFoodRecord = (recordId, recordData) => {
  return api.put(`api/record/update?id=${recordId}`, recordData)
}

// 获取当日食物记录
const getDailyFoodRecords = () => {
  return api.get('api/record/getDaily')
}

// 获取指定日期的食物记录
const getFoodRecordsByDate = (date) => {
  return api.get('api/record/getDaily', { date })
}

module.exports = {
  addFoodRecord,
  updateFoodRecord,
  getDailyFoodRecords,
  getFoodRecordsByDate
} 
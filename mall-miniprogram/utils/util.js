const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatDate = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()

  return `${year}年${formatNumber(month)}月${formatNumber(day)}日`
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

// 计算营养进度百分比
const calculatePercentage = (current, target) => {
  if (!target || target <= 0) return 0
  const percentage = (current / target) * 100
  return percentage > 100 ? 100 : percentage
}

module.exports = {
  formatTime,
  formatDate,
  formatNumber,
  calculatePercentage
}
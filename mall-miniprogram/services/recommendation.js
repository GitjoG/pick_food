const api = require('./api')

// 获取食物推荐
const getFoodRecommendation = (params) => {
  return api.post('api/recommendation/generate', params)
}

// 调整食物推荐
const adjustFoodRecommendation = (recommendationId, adjustParams) => {
  return api.post('api/recommendation/adjust', {
    recommendationId,
    ...adjustParams
  })
}

// 获取餐厅列表
const getRestaurantList = () => {
  return api.get('api/restaurant/list')
}

// 获取餐厅菜单
const getRestaurantMenu = (restaurantId) => {
  return api.get('api/restaurant/menu', { restaurantId })
}

module.exports = {
  getFoodRecommendation,
  adjustFoodRecommendation,
  getRestaurantList,
  getRestaurantMenu
} 
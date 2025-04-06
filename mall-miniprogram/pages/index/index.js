// 首页
const app = getApp()
const nutritionService = require('../../services/nutrition')
const recordService = require('../../services/record')
const recommendationService = require('../../services/recommendation')
const util = require('../../utils/util')

Page({
  data: {
    // 用户信息
    userInfo: null,
    // 今日营养概览
    nutritionOverview: {
      calories: {
        current: 0,
        target: 2000,
        percentage: 0
      },
      protein: {
        current: 0,
        target: 125
      },
      fat: {
        current: 0,
        target: 83
      },
      carbs: {
        current: 0,
        target: 313
      },
      remaining: 0
    },
    // 今日食物记录
    foodRecords: [],
    // 推荐食物组合
    foodRecommendations: [],
    // 页面加载状态
    loading: true
  },

  onLoad: function () {
    this.fetchData()
  },

  onShow: function () {
    // 每次页面显示时刷新数据
    this.fetchData()
  },

  // 获取页面所需数据
  fetchData: function () {
    wx.showLoading({
      title: '加载中',
    })

    Promise.all([
      this.fetchNutritionOverview(),
      this.fetchFoodRecords(),
      this.fetchFoodRecommendations()
    ]).then(() => {
      this.setData({
        loading: false
      })
      wx.hideLoading()
    }).catch(err => {
      console.error('获取数据失败:', err)
      wx.hideLoading()
      wx.showToast({
        title: '获取数据失败',
        icon: 'none'
      })
    })
  },

  // 获取营养概览
  fetchNutritionOverview: function () {
    return new Promise((resolve, reject) => {
      // 模拟数据，实际项目中应该调用API
      setTimeout(() => {
        const nutritionOverview = {
          calories: {
            current: 1200,
            target: 2000,
            percentage: 60
          },
          protein: {
            current: 62,
            target: 125
          },
          fat: {
            current: 50,
            target: 83
          },
          carbs: {
            current: 156,
            target: 313
          },
          remaining: 800
        }
        
        this.setData({
          nutritionOverview
        })
        resolve()
      }, 500)
      
      // 实际项目中的API调用
      // nutritionService.getDailyNutrition()
      //   .then(res => {
      //     // 处理返回数据
      //     const nutritionOverview = {
      //       calories: {
      //         current: res.calories.current,
      //         target: res.calories.target,
      //         percentage: util.calculatePercentage(res.calories.current, res.calories.target)
      //       },
      //       protein: {
      //         current: res.protein.current,
      //         target: res.protein.target
      //       },
      //       fat: {
      //         current: res.fat.current,
      //         target: res.fat.target
      //       },
      //       carbs: {
      //         current: res.carbs.current,
      //         target: res.carbs.target
      //       },
      //       remaining: res.calories.target - res.calories.current
      //     }
      //     
      //     this.setData({
      //       nutritionOverview
      //     })
      //     resolve()
      //   })
      //   .catch(err => {
      //     console.error('获取营养概览失败:', err)
      //     reject(err)
      //   })
    })
  },

  // 获取食物记录
  fetchFoodRecords: function () {
    return new Promise((resolve, reject) => {
      // 模拟数据，实际项目中应该调用API
      setTimeout(() => {
        const foodRecords = [
          {
            mealType: '早餐',
            mealTime: '8:00',
            foods: [
              { name: '全麦面包', quantity: '2片' },
              { name: '煮鸡蛋', quantity: '2个' }
            ],
            calories: 300
          },
          {
            mealType: '午餐',
            mealTime: '12:30',
            foods: [
              { name: '烤鸡沙拉', quantity: '' },
              { name: '无糖冰美式', quantity: '' },
              { name: '蒸鸡胸肉', quantity: '' },
              { name: '糙米饭', quantity: '小份' }
            ],
            calories: 605
          },
          {
            mealType: '下午茶',
            mealTime: '15:30',
            foods: [
              { name: '希腊酸奶', quantity: '' },
              { name: '蓝莓', quantity: '100g' }
            ],
            calories: 210
          }
        ]
        
        this.setData({
          foodRecords
        })
        resolve()
      }, 500)
      
      // 实际项目中的API调用
      // recordService.getDailyFoodRecords()
      //   .then(res => {
      //     this.setData({
      //       foodRecords: res.records || []
      //     })
      //     resolve()
      //   })
      //   .catch(err => {
      //     console.error('获取食物记录失败:', err)
      //     reject(err)
      //   })
    })
  },

  // 获取食物推荐
  fetchFoodRecommendations: function () {
    return new Promise((resolve, reject) => {
      // 模拟数据，实际项目中应该调用API
      setTimeout(() => {
        const foodRecommendations = [
          {
            mealType: '晚餐推荐',
            remainingCalories: 800,
            foods: [
              { name: '健身餐厅 - 烤三文鱼', quantity: '' },
              { name: '健身餐厅 - 藜麦饭', quantity: '小份' }
            ],
            calories: 370
          }
        ]
        
        this.setData({
          foodRecommendations
        })
        resolve()
      }, 500)
      
      // 实际项目中的API调用
      // recommendationService.getFoodRecommendation({
      //   remainingCalories: this.data.nutritionOverview.remaining
      // })
      //   .then(res => {
      //     this.setData({
      //       foodRecommendations: res.recommendations || []
      //     })
      //     resolve()
      //   })
      //   .catch(err => {
      //     console.error('获取食物推荐失败:', err)
      //     reject(err)
      //   })
    })
  },

  // 跳转到食物推荐页
  navigateToFoodRecommend: function () {
    wx.navigateTo({
      url: '/pages/food-recommend/food-recommend'
    })
  },

  // 跳转到记录食物页
  navigateToAddRecord: function () {
    wx.navigateTo({
      url: '/pages/add-record/add-record'
    })
  },

  // 跳转到营养目标页
  navigateToNutritionCalc: function () {
    wx.navigateTo({
      url: '/pages/nutrition-calc/nutrition-calc'
    })
  },

  // 跳转到附近餐厅页
  navigateToRestaurantSelect: function () {
    wx.navigateTo({
      url: '/pages/restaurant-select/restaurant-select'
    })
  },

  // 跳转到食物记录页
  navigateToFoodRecord: function () {
    wx.navigateTo({
      url: '/pages/food-record/food-record'
    })
  },

  // 跳转到更多推荐页
  navigateToMoreRecommendations: function () {
    wx.navigateTo({
      url: '/pages/food-recommend/food-recommend'
    })
  },

  // 处理餐食记录点击
  handleMealTap: function (e) {
    const mealData = e.detail
    wx.navigateTo({
      url: `/pages/add-record/add-record?mealType=${mealData.mealType}&mealTime=${mealData.mealTime}`
    })
  }
}) 
// 营养目标计算页面
const app = getApp()
const nutritionService = require('../../services/nutrition')

Page({
  data: {
    // 用户输入数据
    userInfo: {
      height: '',
      weight: '',
      age: '',
      gender: 'male', // 默认男性
      activity_level: 'moderate', // 默认中等活动量
      goal: 'maintain' // 默认维持体重
    },
    // 计算结果
    nutritionGoals: null,
    // 活动量选项
    activityOptions: [
      { value: 'sedentary', label: '久坐不动 (几乎不运动)' },
      { value: 'light', label: '轻度活动 (每周运动1-3次)' },
      { value: 'moderate', label: '中度活动 (每周运动3-5次)' },
      { value: 'active', label: '重度活动 (每周运动6-7次)' },
      { value: 'very_active', label: '极度活动 (每天高强度运动)' }
    ],
    // 目标选项
    goalOptions: [
      { value: 'lose', label: '减脂 (减少体重)' },
      { value: 'maintain', label: '维持 (保持体重)' },
      { value: 'gain', label: '增肌 (增加体重)' }
    ],
    // 选择器索引
    activityLevelIndex: 2, // 默认中等活动量
    goalIndex: 1, // 默认维持体重
    // 页面状态
    calculating: false,
    showResult: false,
    errorMsg: ''
  },

  onLoad: function (options) {
    // 尝试获取已有的用户信息
    const userInfo = wx.getStorageSync('userInfo')
    if (userInfo) {
      // 设置活动量索引
      let activityLevelIndex = 2; // 默认中等活动量
      for (let i = 0; i < this.data.activityOptions.length; i++) {
        if (this.data.activityOptions[i].value === userInfo.activity_level) {
          activityLevelIndex = i;
          break;
        }
      }
      
      // 设置目标索引
      let goalIndex = 1; // 默认维持体重
      for (let i = 0; i < this.data.goalOptions.length; i++) {
        if (this.data.goalOptions[i].value === userInfo.goal) {
          goalIndex = i;
          break;
        }
      }
      
      this.setData({
        'userInfo.height': userInfo.height || '',
        'userInfo.weight': userInfo.weight || '',
        'userInfo.age': userInfo.age || '',
        'userInfo.gender': userInfo.gender || 'male',
        'userInfo.activity_level': userInfo.activity_level || 'moderate',
        'userInfo.goal': userInfo.goal || 'maintain',
        activityLevelIndex,
        goalIndex
      })
    }
  },

  // 输入框变化处理
  handleInputChange: function (e) {
    const { field } = e.currentTarget.dataset
    const { value } = e.detail
    
    this.setData({
      [`userInfo.${field}`]: value
    })
  },

  // 单选框变化处理
  handleRadioChange: function (e) {
    const { field } = e.currentTarget.dataset
    const { value } = e.detail
    
    if (field === 'activity_level') {
      // 修复活动量选择问题：这里value是索引，需要获取实际的活动量值
      const selectedIndex = parseInt(value);
      const selectedValue = this.data.activityOptions[selectedIndex].value;
      
      this.setData({
        [`userInfo.${field}`]: selectedValue,
        activityLevelIndex: selectedIndex
      })
    } else if (field === 'goal') {
      // 更新目标索引
      const selectedIndex = parseInt(value);
      const selectedValue = this.data.goalOptions[selectedIndex].value;
      
      this.setData({
        [`userInfo.${field}`]: selectedValue,
        goalIndex: selectedIndex
      })
    } else {
      this.setData({
        [`userInfo.${field}`]: value
      })
    }
  },

  // 表单提交
  handleSubmit: function () {
    // 验证表单
    const { height, weight, age, gender, activity_level, goal } = this.data.userInfo
    
    if (!height || !weight || !age) {
      this.setData({
        errorMsg: '请填写完整的身体数据'
      })
      return
    }
    
    if (height <= 0 || weight <= 0 || age <= 0) {
      this.setData({
        errorMsg: '身高、体重和年龄必须大于0'
      })
      return
    }
    
    // 清除错误信息
    this.setData({
      errorMsg: '',
      calculating: true
    })
    
    // 调用API计算营养目标
    nutritionService.calculateAll({
      height: parseFloat(height),
      weight: parseFloat(weight),
      age: parseInt(age),
      gender,
      activity_level,
      goal
    }).then(res => {
      console.log('计算结果:', res)
      
      // 保存计算结果
      const nutritionGoals = {
        bmr: res.bmr,
        tdee: res.tdee,
        calories: res.calorie_target,
        protein: res.protein,
        fat: res.fat,
        carbs: res.carb
      }
      
      // 更新全局数据
      app.globalData.nutritionGoals = nutritionGoals
      
      // 保存用户信息到本地
      wx.setStorageSync('userInfo', this.data.userInfo)
      wx.setStorageSync('nutritionGoals', nutritionGoals)
      
      this.setData({
        nutritionGoals,
        calculating: false,
        showResult: true
      })
    }).catch(err => {
      console.error('计算失败:', err)
      this.setData({
        errorMsg: '计算失败，请重试',
        calculating: false
      })
    })
  },

  // 返回首页
  navigateToHome: function () {
    wx.switchTab({
      url: '/pages/index/index'
    })
  }
}) 
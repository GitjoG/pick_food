// pages/profile/profile.js
const app = getApp()
const storage = require('../../utils/storage')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: null,
    hasUserInfo: false,
    canIUseGetUserProfile: false,
    nutritionGoals: null,
    // 设置项
    settingsList: [
      {
        id: 'nutrition',
        icon: '/assets/icons/nutrition.png',
        text: '身体参数设置',
        url: '/pages/nutrition-calc/nutrition-calc'
      },
      {
        id: 'history',
        icon: '/assets/icons/record.png',
        text: '历史记录',
        url: '/pages/history/history'
      },
      {
        id: 'about',
        icon: '/assets/icons/about.png',
        text: '关于我们',
        url: '/pages/about/about'
      },
      {
        id: 'feedback',
        icon: '/assets/icons/feedback.png',
        text: '意见反馈',
        url: '/pages/feedback/feedback'
      }
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
    
    // 获取用户信息
    this.getUserInfo()
    
    // 获取营养目标
    this.getNutritionGoals()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    // 每次显示页面时刷新数据
    this.getNutritionGoals()
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  // 获取用户信息
  getUserInfo: function (e) {
    // 如果是从按钮触发的
    if (e && e.detail && e.detail.userInfo) {
      const userInfo = {
        ...e.detail.userInfo,
        // 添加默认身体数据
        height: '',
        weight: '',
        age: '',
        gender: e.detail.userInfo.gender === 1 ? 'male' : 'female',
        activity_level: 'moderate',
        goal: 'maintain'
      }
      
      storage.saveUserInfo(userInfo)
      
      this.setData({
        userInfo,
        hasUserInfo: true
      })
      
      // 引导用户设置营养目标
      this.showNutritionGoalPrompt()
      
      return
    }
    
    // 否则从缓存获取
    const userInfo = storage.getUserInfo()
    if (userInfo) {
      this.setData({
        userInfo,
        hasUserInfo: true
      })
    }
  },
  
  // 获取用户营养目标
  getNutritionGoals: function () {
    const nutritionGoals = storage.getNutritionGoals() || app.globalData.nutritionGoals
    if (nutritionGoals) {
      this.setData({
        nutritionGoals
      })
    }
  },
  
  // 使用微信接口获取用户信息
  getUserProfile: function () {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        const userInfo = {
          ...res.userInfo,
          // 添加默认身体数据
          height: '',
          weight: '',
          age: '',
          gender: res.userInfo.gender === 1 ? 'male' : 'female',
          activity_level: 'moderate',
          goal: 'maintain'
        }
        
        // 保存用户信息
        storage.saveUserInfo(userInfo)
        
        this.setData({
          userInfo,
          hasUserInfo: true
        })
        
        // 引导用户设置营养目标
        this.showNutritionGoalPrompt()
      },
      fail: (err) => {
        console.log('获取用户信息失败', err)
        
        // 使用默认信息
        const userInfo = {
          nickName: '用户名',
          avatarUrl: '/assets/icons/default-avatar.png',
          // 添加默认身体数据
          height: '',
          weight: '',
          age: '',
          gender: 'unknown',
          activity_level: 'moderate',
          goal: 'maintain'
        }
        
        // 保存用户信息
        storage.saveUserInfo(userInfo)
        
        this.setData({
          userInfo,
          hasUserInfo: true
        })
        
        // 引导用户设置营养目标
        this.showNutritionGoalPrompt()
      }
    })
  },
  
  // 显示营养目标提示
  showNutritionGoalPrompt: function() {
    wx.showModal({
      title: '设置营养目标',
      content: '是否现在设置您的营养目标？',
      confirmText: '立即设置',
      cancelText: '稍后设置',
      success: (res) => {
        if (res.confirm) {
          wx.navigateTo({
            url: '/pages/nutrition-calc/nutrition-calc'
          })
        }
      }
    })
  },
  
  // 点击设置项
  handleSettingTap: function (e) {
    const { url } = e.currentTarget.dataset
    wx.navigateTo({
      url
    })
  },
  
  // 退出登录
  handleLogout: function () {
    wx.showModal({
      title: '退出登录',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清除用户信息
          storage.clearStorage()
          
          // 重置数据
          this.setData({
            userInfo: null,
            hasUserInfo: false,
            nutritionGoals: null
          })
          
          // 重置全局数据
          app.globalData.userInfo = null
          app.globalData.nutritionGoals = {
            calories: 2000,
            protein: 125,
            fat: 83,
            carbs: 313
          }
          
          wx.showToast({
            title: '已退出登录',
            icon: 'success'
          })
        }
      }
    })
  }
})
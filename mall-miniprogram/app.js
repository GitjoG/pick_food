// app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    
    // 在全局数据设置完成后，再引入用户服务并执行登录
    setTimeout(() => {
      const userService = require('./services/user.js');
      
      // 检查登录状态，强制重新登录以获取新token
      this.autoLogin();
    }, 0);
  },
  
  // 自动登录方法
  autoLogin: function() {
    console.log('自动登录开始');
    const baseUrl = this.globalData.baseUrl;
    
    wx.request({
      url: `${baseUrl}/api/user/test_login`,
      method: 'POST',
      success: (res) => {
        console.log('自动登录成功:', res.data);
        if (res.data.code === 0 && res.data.data && res.data.data.token) {
          wx.setStorageSync('token', res.data.data.token);
          console.log('自动登录成功，token已保存');
        }
      },
      fail: (err) => {
        console.error('自动登录失败:', err);
      }
    });
  },
  
  globalData: {
    userInfo: null,
    baseUrl: 'http://localhost:4000',
    // 默认营养目标
    nutritionGoals: {
      calories: 2000,
      protein: 125,
      fat: 83,
      carbs: 313
    }
  }
}) 
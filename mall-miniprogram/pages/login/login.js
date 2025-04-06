// 引入用户服务
const userService = require('../../services/user.js');

Page({
  data: {
    isLoading: false
  },
  
  onLoad: function() {
    // 页面加载时检查登录状态
    if (userService.checkLoginStatus()) {
      // 已登录，跳转到首页或其他页面
      wx.switchTab({
        url: '/pages/index/index'
      });
    }
  },
  
  // 登录按钮点击事件
  handleLogin: function() {
    this.setData({ isLoading: true });
    
    userService.login()
      .then(res => {
        this.setData({ isLoading: false });
        // 登录成功，跳转到首页
        wx.switchTab({
          url: '/pages/index/index'
        });
      })
      .catch(err => {
        this.setData({ isLoading: false });
        wx.showToast({
          title: '登录失败',
          icon: 'none'
        });
        console.error('登录失败', err);
      });
  }
}); 
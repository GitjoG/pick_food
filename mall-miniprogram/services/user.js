// 创建用户服务文件
const userService = {
  // 获取基础URL
  getBaseUrl: function() {
    const app = getApp();
    return app.globalData.baseUrl || 'https://your-server.com/api';
  },
  
  // 登录方法
  login: function() {
    console.log('开始登录流程');
    return new Promise((resolve, reject) => {
      wx.login({
        success: function(res) {
          console.log('wx.login成功，获取到code:', res.code);
          if (res.code) {
            // 获取到code后发送到后端
            const url = `${userService.getBaseUrl()}/user/login`;
            console.log('准备发送请求到后端:', url);
            wx.request({
              url: url,
              method: 'POST',
              data: {
                code: res.code
              },
              success: function(response) {
                console.log('后端返回状态码:', response.statusCode);
                console.log('后端返回数据:', response.data);
                
                if (response.statusCode !== 200) {
                  console.error('请求失败:', response.data);
                  reject(new Error(response.data.error || '登录失败'));
                  return;
                }
                
                // 保存返回的token或用户信息
                if (response.data.token) {
                  wx.setStorageSync('token', response.data.token);
                  console.log('保存token成功');
                }
                if (response.data.userInfo) {
                  wx.setStorageSync('userInfo', response.data.userInfo);
                  console.log('保存用户信息成功');
                }
                resolve(response.data);
              },
              fail: function(err) {
                console.error('请求后端失败:', err);
                reject(err);
              }
            });
          } else {
            console.error('获取code失败:', res.errMsg);
            reject(new Error('登录失败: ' + res.errMsg));
          }
        },
        fail: function(err) {
          console.error('wx.login调用失败:', err);
          reject(err);
        }
      });
    });
  },
  
  // 检查登录状态
  checkLoginStatus: function() {
    const token = wx.getStorageSync('token');
    return !!token;
  },

  // 获取用户信息
  getUserInfo: function() {
    const token = wx.getStorageSync('token');
    if (!token) {
      return Promise.reject(new Error('未登录'));
    }
    
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${userService.getBaseUrl()}/user/userinfo`,
        method: 'GET',
        header: {
          'Authorization': `Bearer ${token}`
        },
        success: function(res) {
          if (res.statusCode === 200) {
            // 更新本地存储的用户信息
            wx.setStorageSync('userInfo', res.data.user);
            resolve(res.data.user);
          } else {
            reject(new Error(res.data.error || '获取用户信息失败'));
          }
        },
        fail: function(err) {
          reject(err);
        }
      });
    });
  },

  // 更新用户信息
  updateUserInfo: function(userInfo) {
    const token = wx.getStorageSync('token');
    if (!token) {
      return Promise.reject(new Error('未登录'));
    }
    
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${userService.getBaseUrl()}/user/info`,
        method: 'PUT',
        header: {
          'Authorization': `Bearer ${token}`
        },
        data: userInfo,
        success: function(res) {
          if (res.statusCode === 200) {
            // 更新本地存储的用户信息
            const oldUserInfo = wx.getStorageSync('userInfo') || {};
            wx.setStorageSync('userInfo', {...oldUserInfo, ...userInfo});
            resolve(res.data);
          } else {
            reject(new Error(res.data.error || '更新用户信息失败'));
          }
        },
        fail: function(err) {
          reject(err);
        }
      });
    });
  }
};

module.exports = userService; 
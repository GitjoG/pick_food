const app = getApp()

// 基础请求方法
const request = (url, method, data) => {
  // 确保URL格式正确，防止双斜杠问题
  const baseUrl = app.globalData.baseUrl;
  const formattedUrl = url.startsWith('/') ? url : `/${url}`;
  const fullUrl = `${baseUrl}${formattedUrl}`;
  
  console.log(`发起请求: ${method} ${fullUrl}`, data);
  
  // 获取token（如果有）
  const token = wx.getStorageSync('token');
  const headers = {
    'content-type': 'application/json'
  };
  
  // 如果有token，添加到请求头
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return new Promise((resolve, reject) => {
    wx.request({
      url: fullUrl,
      method,
      data,
      header: headers,
      success: (res) => {
        console.log(`请求成功: ${method} ${url}`, res);
        
        if (res.statusCode === 200 || res.data.code === 0) {
          resolve(res.data)
        } else {
          const errorMsg = res.data && res.data.message ? res.data.message : `请求失败，状态码: ${res.statusCode}`;
          console.error(`请求失败: ${method} ${url}`, errorMsg);
          reject(new Error(errorMsg));
        }
      },
      fail: (err) => {
        console.error(`请求错误: ${method} ${url}`, err);
        // 显示错误提示
        wx.showToast({
          title: `网络请求失败: ${err.errMsg}`,
          icon: 'none',
          duration: 2000
        });
        reject(err)
      }
    })
  })
}

// GET请求
const get = (url, params = {}) => {
  let queryString = ''
  if (Object.keys(params).length > 0) {
    queryString = '?' + Object.keys(params)
      .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
      .join('&')
  }
  return request(`${url}${queryString}`, 'GET')
}

// POST请求
const post = (url, data) => {
  return request(url, 'POST', data)
}

// PUT请求
const put = (url, data) => {
  return request(url, 'PUT', data)
}

// DELETE请求
const del = (url) => {
  return request(url, 'DELETE')
}

module.exports = {
  get,
  post,
  put,
  delete: del
} 
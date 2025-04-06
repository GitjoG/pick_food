// pages/food-recommend/food-recommend.js
const app = getApp()
const util = require('../../utils/util')
const recommendationService = require('../../services/recommendation')
const recordService = require('../../services/record')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 当前显示的页面：params(参数设置), results(推荐结果), adjust(调整组合)
    currentPage: 'params',
    
    // 营养目标
    nutritionGoals: {
      calories: 2000,
      protein: 125,
      fat: 83,
      carbs: 313
    },
    
    // 餐厅偏好
    restaurants: ['请选择', '麦当劳', '健身餐厅', '沙拉专卖', '中式快餐'],
    preferredIndex: 0,
    excludedIndex: 0,
    
    // 餐次占比
    ratios: ['20%', '30% (默认)', '40%', '50%'],
    ratioIndex: 1,
    mealRatio: '30%',
    
    // 推荐的食物
    recommendedFoods: [
      {
        restaurant: '麦当劳',
        foods: [
          {
            name: '烤鸡沙拉',
            calories: 300,
            protein: 25,
            fat: 10,
            carbs: 30,
            selected: true
          },
          {
            name: '无糖冰美式',
            calories: 5,
            protein: 0,
            fat: 0,
            carbs: 1,
            selected: true
          }
        ]
      },
      {
        restaurant: '健身餐厅',
        foods: [
          {
            name: '蒸鸡胸肉',
            calories: 200,
            protein: 40,
            fat: 5,
            carbs: 0,
            selected: true
          },
          {
            name: '糙米饭(小份)',
            calories: 100,
            protein: 2,
            fat: 1,
            carbs: 22,
            selected: true
          }
        ]
      }
    ],
    
    // 替代食物
    alternativeFoods: [
      {
        restaurant: '麦当劳',
        foods: [
          {
            name: '凯撒沙拉',
            calories: 350,
            protein: 20,
            fat: 20,
            carbs: 25,
            selected: false
          },
          {
            name: '水果茶',
            calories: 120,
            protein: 0,
            fat: 0,
            carbs: 30,
            selected: false
          }
        ]
      },
      {
        restaurant: '健身餐厅',
        foods: [
          {
            name: '烤三文鱼',
            calories: 250,
            protein: 30,
            fat: 15,
            carbs: 0,
            selected: false
          },
          {
            name: '藜麦饭(小份)',
            calories: 120,
            protein: 4,
            fat: 2,
            carbs: 20,
            selected: false
          }
        ]
      }
    ],
    
    // 营养总计
    totalNutrition: {
      calories: 605,
      protein: 67,
      fat: 16,
      carbs: 53
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    // 获取全局营养目标
    const globalData = app.globalData;
    if (globalData && globalData.nutritionGoals) {
      this.setData({
        nutritionGoals: globalData.nutritionGoals
      });
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {
    // 这里可以添加从服务器获取真实数据的代码
    // this.fetchNutritionGoals();
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
  
  // 返回上一页
  navigateBack: function() {
    // 如果当前在参数页，返回首页
    if (this.data.currentPage === 'params') {
      wx.navigateBack();
    } 
    // 如果当前在结果页，返回参数页
    else if (this.data.currentPage === 'results') {
      this.setData({
        currentPage: 'params'
      });
    } 
    // 如果当前在调整页，返回结果页
    else if (this.data.currentPage === 'adjust') {
      this.setData({
        currentPage: 'results'
      });
    }
  },
  
  // 想吃餐厅选择变化
  bindPreferredChange: function(e) {
    this.setData({
      preferredIndex: e.detail.value
    });
  },
  
  // 不想吃餐厅选择变化
  bindExcludedChange: function(e) {
    this.setData({
      excludedIndex: e.detail.value
    });
  },
  
  // 餐次占比选择变化
  bindRatioChange: function(e) {
    const ratioIndex = e.detail.value;
    const mealRatio = this.data.ratios[ratioIndex];
    
    this.setData({
      ratioIndex: ratioIndex,
      mealRatio: mealRatio
    });
  },
  
  // 生成推荐
  generateRecommendation: function() {
    // 显示加载提示
    wx.showLoading({
      title: '生成推荐中...',
    });
    
    // 获取当前选择的参数
    const { 
      preferredIndex, 
      excludedIndex, 
      ratioIndex, 
      restaurants, 
      ratios,
      nutritionGoals
    } = this.data;
    
    // 解析餐次占比百分比
    const ratioStr = ratios[ratioIndex];
    const ratio = parseInt(ratioStr.replace('%', '')) / 100;
    
    // 计算目标热量
    const targetCalories = Math.round(nutritionGoals.calories * ratio);
    
    // 构造请求参数
    const params = {
      preferredRestaurant: preferredIndex > 0 ? restaurants[preferredIndex] : null,
      excludedRestaurant: excludedIndex > 0 ? restaurants[excludedIndex] : null,
      targetCalories: targetCalories,
      targetProtein: Math.round(nutritionGoals.protein * ratio),
      targetFat: Math.round(nutritionGoals.fat * ratio),
      targetCarbs: Math.round(nutritionGoals.carbs * ratio)
    };
    
    // 这里可以添加实际从服务器获取食物推荐的代码
    // recommendationService.getFoodRecommendation(params)
    //   .then(res => {
    //     this.processRecommendationResult(res);
    //     wx.hideLoading();
    //   })
    //   .catch(err => {
    //     console.error('获取推荐失败:', err);
    //     wx.hideLoading();
    //     wx.showToast({
    //       title: '获取推荐失败',
    //       icon: 'none'
    //     });
    //   });
    
    // 模拟获取推荐结果
    setTimeout(() => {
      // 使用模拟数据
      const recommendedFoods = this.data.recommendedFoods;
      const totalNutrition = this.calculateTotalNutrition(recommendedFoods);
      
      this.setData({
        currentPage: 'results',
        totalNutrition: totalNutrition
      });
      
      wx.hideLoading();
    }, 1000);
  },
  
  // 处理推荐结果
  processRecommendationResult: function(result) {
    // 设置推荐食物和总营养
    this.setData({
      currentPage: 'results',
      recommendedFoods: result.foods,
      totalNutrition: result.totalNutrition
    });
  },
  
  // 调整组合
  adjustCombination: function() {
    this.setData({
      currentPage: 'adjust'
    });
  },
  
  // 记录这一餐
  recordMeal: function() {
    // 显示加载提示
    wx.showLoading({
      title: '记录中...',
    });
    
    // 获取当前选中的食物
    const { recommendedFoods, totalNutrition } = this.data;
    
    // 构造餐食记录对象
    const mealRecord = {
      mealType: '午餐', // 这里可以根据实际情况设置
      mealTime: util.formatTime(new Date()).split(' ')[1].substring(0, 5),
      foods: [],
      totalNutrition: totalNutrition
    };
    
    // 收集所有选中的食物
    recommendedFoods.forEach(restaurant => {
      restaurant.foods.forEach(food => {
        if (food.selected !== false) { // 默认全部选中
          mealRecord.foods.push({
            name: food.name,
            quantity: '',
            calories: food.calories,
            protein: food.protein,
            fat: food.fat,
            carbs: food.carbs
          });
        }
      });
    });
    
    // 这里可以添加实际保存记录的代码
    // recordService.addFoodRecord(mealRecord)
    //   .then(res => {
    //     wx.hideLoading();
    //     wx.showToast({
    //       title: '记录成功',
    //       icon: 'success'
    //     });
    //     // 返回首页
    //     wx.navigateBack();
    //   })
    //   .catch(err => {
    //     console.error('记录失败:', err);
    //     wx.hideLoading();
    //     wx.showToast({
    //       title: '记录失败',
    //       icon: 'none'
    //     });
    //   });
    
    // 模拟保存记录
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '记录成功',
        icon: 'success'
      });
      
      // 返回首页
      wx.navigateBack();
    }, 1000);
  },
  
  // 切换食物选择状态
  toggleFoodSelection: function(e) {
    const { restaurant, index } = e.currentTarget.dataset;
    const foodPath = `recommendedFoods[${this.findRestaurantIndex(restaurant, 'recommendedFoods')}].foods[${index}].selected`;
    const currentValue = this.getValueFromPath(foodPath);
    
    // 更新选择状态
    const update = {};
    update[foodPath] = !currentValue;
    this.setData(update);
    
    // 重新计算营养总计
    this.updateTotalNutrition();
  },
  
  // 切换替代食物选择状态
  toggleAlternativeSelection: function(e) {
    const { restaurant, index } = e.currentTarget.dataset;
    const foodPath = `alternativeFoods[${this.findRestaurantIndex(restaurant, 'alternativeFoods')}].foods[${index}].selected`;
    const currentValue = this.getValueFromPath(foodPath);
    
    // 更新选择状态
    const update = {};
    update[foodPath] = !currentValue;
    this.setData(update);
    
    // 重新计算营养总计
    this.updateTotalNutrition();
  },
  
  // 确认调整
  confirmAdjustment: function() {
    // 更新选中的食物
    this.updateSelectedFoods();
    
    // 返回结果页
    this.setData({
      currentPage: 'results'
    });
  },
  
  // 更新选中的食物
  updateSelectedFoods: function() {
    // 重新计算营养总计
    const totalNutrition = this.calculateTotalNutrition([
      ...this.data.recommendedFoods,
      ...this.data.alternativeFoods
    ]);
    
    // 更新总营养
    this.setData({
      totalNutrition: totalNutrition
    });
  },
  
  // 计算总营养
  calculateTotalNutrition: function(foodGroups) {
    let calories = 0;
    let protein = 0;
    let fat = 0;
    let carbs = 0;
    
    // 遍历所有食物组
    foodGroups.forEach(group => {
      // 遍历组内所有食物
      group.foods.forEach(food => {
        // 只计算选中的食物
        if (food.selected !== false) {
          calories += food.calories || 0;
          protein += food.protein || 0;
          fat += food.fat || 0;
          carbs += food.carbs || 0;
        }
      });
    });
    
    return {
      calories,
      protein,
      fat,
      carbs
    };
  },
  
  // 更新总营养计算
  updateTotalNutrition: function() {
    const totalNutrition = this.calculateTotalNutrition([
      ...this.data.recommendedFoods,
      ...this.data.alternativeFoods
    ]);
    
    this.setData({
      totalNutrition: totalNutrition
    });
  },
  
  // 查找餐厅在数组中的索引
  findRestaurantIndex: function(name, arrayName) {
    const array = this.data[arrayName];
    for (let i = 0; i < array.length; i++) {
      if (array[i].restaurant === name) {
        return i;
      }
    }
    return -1;
  },
  
  // 根据路径获取值
  getValueFromPath: function(path) {
    const parts = path.split('.');
    let value = this.data;
    
    for (const part of parts) {
      // 处理数组索引
      const match = part.match(/^([^\[]+)\[(\d+)\]$/);
      if (match) {
        const arrayName = match[1];
        const index = parseInt(match[2]);
        value = value[arrayName][index];
      } else {
        value = value[part];
      }
      
      if (value === undefined) {
        return undefined;
      }
    }
    
    return value;
  }
})
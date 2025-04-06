// pages/food-record/food-record.js
const app = getApp()
const util = require('../../utils/util')
const recordService = require('../../services/record')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    currentDate: '',
    selectedDate: '', // 当前选中的日期
    weekDays: [], // 一周日期数组
    
    // 月日历相关
    showMonthCalendar: false, // 是否显示月日历
    currentYearMonth: '', // 当前显示的年月
    currentMonth: null, // 当前显示的月份对象
    monthDays: [], // 月日历数据
    
    // 交互相关
    touchStartX: 0, // 触摸开始位置
    touchEndX: 0, // 触摸结束位置
    weekAnimation: null, // 周日历动画
    monthAnimation: null, // 月日历动画
    
    // 编辑模式
    isEditMode: false, // 是否处于编辑模式
    
    // 拖拽相关
    isDragging: false, // 是否正在拖拽
    dragStartY: 0, // 拖拽开始的Y坐标
    dragCurY: 0, // 当前拖拽的Y坐标
    dragMealIndex: -1, // 当前拖拽餐次索引
    dragFoodIndex: -1, // 当前拖拽食物索引
    dragItemHeight: 0, // 拖拽项目高度
    dragItemTop: 0, // 拖拽项目顶部位置
    dragItemLeft: 0, // 拖拽项目左侧位置
    
    // 营养数据
    nutritionData: {
      calories: {
        current: 0,
        target: 0,
        percentage: 0
      },
      protein: {
        current: 0,
        target: 0,
        percentage: 0
      },
      fat: {
        current: 0,
        target: 0,
        percentage: 0
      },
      carbs: {
        current: 0,
        target: 0,
        percentage: 0
      },
      remaining: 0
    },
    // 食物记录
    foodRecords: [],
    hasDinner: false,
    // 添加食物弹窗
    showAddModal: false,
    mealTypes: ['早餐', '午餐', '下午茶', '晚餐', '夜宵'],
    mealTypeIndex: 3, // 默认选择晚餐
    mealTime: '18:30',
    foodSource: 'manual',
    newFood: {
      name: '',
      calories: '',
      protein: '',
      fat: '',
      carbs: ''
    },
    editingFoodInfo: null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 获取当前日期
    const today = new Date();
    const formattedDate = util.formatDate(today);
    
    // 创建动画实例
    this.weekAnimationInstance = wx.createAnimation({
      duration: 300,
      timingFunction: 'ease',
    });
    
    this.monthAnimationInstance = wx.createAnimation({
      duration: 300,
      timingFunction: 'ease',
    });
    
    this.setData({
      currentDate: formattedDate,
      selectedDate: formattedDate,
      currentYearMonth: `${today.getFullYear()}年${util.formatNumber(today.getMonth() + 1)}月`,
      currentMonth: today
    });
    
    // 生成一周日期数据
    this.generateWeekDays(today);
    
    // 生成月日历数据
    this.generateMonthDays(today);
    
    // 从API获取当前日期记录和有记录的日期
    this.fetchFoodRecords(formattedDate);
    this.fetchNutritionData(formattedDate);
    this.fetchRecordDates(today.getFullYear(), today.getMonth() + 1);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    // 每次显示页面时刷新数据
    this.fetchFoodRecords(this.data.selectedDate);
    this.fetchNutritionData(this.data.selectedDate);
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
  
  // 检查是否有晚餐记录
  checkHasDinner: function() {
    const hasDinner = this.data.foodRecords.some(item => item.mealType === '晚餐')
    this.setData({ hasDinner })
  },
  
  // 获取前一天记录
  getPrevDay: function() {
    const currentDate = new Date(this.data.currentDate.replace(/年|月/g, '/').replace('日', ''))
    currentDate.setDate(currentDate.getDate() - 1)
    const formattedDate = util.formatDate(currentDate);
    
    this.setData({
      currentDate: formattedDate,
      selectedDate: formattedDate
    })
    
    // 加载对应日期的数据
    this.fetchFoodRecords(formattedDate);
    this.fetchNutritionData(formattedDate);
  },
  
  // 获取后一天记录
  getNextDay: function() {
    const currentDate = new Date(this.data.currentDate.replace(/年|月/g, '/').replace('日', ''));
    currentDate.setDate(currentDate.getDate() + 1);
    const formattedDate = util.formatDate(currentDate);
    
    this.setData({
      currentDate: formattedDate,
      selectedDate: formattedDate
    });
    
    // 检查是否需要更新周视图
    this.generateWeekDays(currentDate);
    
    // 加载对应日期的数据
    this.fetchFoodRecords(formattedDate);
    this.fetchNutritionData(formattedDate);
  },
  
  // 返回上一页
  navigateBack: function() {
    wx.navigateBack()
  },
  
  // 显示添加食物记录弹窗
  showAddFoodRecord: function() {
    this.setData({
      showAddModal: true,
      newFood: {
        name: '',
        calories: '',
        protein: '',
        fat: '',
        carbs: ''
      }
    })
  },
  
  // 隐藏添加食物记录弹窗
  hideAddFoodRecord: function() {
    this.setData({
      showAddModal: false,
      editingFoodInfo: null
    });
  },
  
  // 阻止点击事件冒泡
  stopPropagation() {
    // 仅用于阻止事件冒泡，无需实际操作
  },
  
  // 餐次选择变化
  bindMealTypeChange: function(e) {
    this.setData({
      mealTypeIndex: e.detail.value
    })
  },
  
  // 时间选择变化
  bindTimeChange: function(e) {
    this.setData({
      mealTime: e.detail.value
    })
  },
  
  // 食物来源选择变化
  bindFoodSourceChange: function(e) {
    this.setData({
      foodSource: e.detail.value
    })
  },
  
  // 食物名称输入
  bindFoodNameInput: function(e) {
    this.setData({
      'newFood.name': e.detail.value
    })
  },
  
  // 热量输入
  bindCaloriesInput: function(e) {
    this.setData({
      'newFood.calories': e.detail.value
    })
  },
  
  // 蛋白质输入
  bindProteinInput: function(e) {
    this.setData({
      'newFood.protein': e.detail.value
    })
  },
  
  // 脂肪输入
  bindFatInput: function(e) {
    this.setData({
      'newFood.fat': e.detail.value
    })
  },
  
  // 碳水输入
  bindCarbsInput: function(e) {
    this.setData({
      'newFood.carbs': e.detail.value
    })
  },
  
  // 选择日期（周日历中选择）
  selectWeekDay: function(e) {
    const index = e.currentTarget.dataset.index;
    const day = this.data.weekDays[index];
    
    this.setData({
      selectedDate: day.date,
      currentDate: day.date
    });
    
    // 加载对应日期的数据
    this.fetchFoodRecords(day.date);
    this.fetchNutritionData(day.date);
  },
  
  // 选择日期（月日历中选择）
  selectMonthDay: function(e) {
    const index = e.currentTarget.dataset.index;
    const day = this.data.monthDays[index];
    
    if (!day.isCurrentMonth) {
      return; // 不允许选择非当前月的日期
    }
    
    const date = new Date(this.data.currentMonth);
    date.setDate(day.day);
    const formattedDate = util.formatDate(date);
    
    this.setData({
      selectedDate: formattedDate,
      currentDate: formattedDate,
      showMonthView: false // 选择后隐藏月视图
    });
    
    // 重新生成周视图，确保选中日期在周视图中可见
    this.generateWeekDays(date);
    
    // 加载对应日期的数据
    this.fetchFoodRecords(formattedDate);
    this.fetchNutritionData(formattedDate);
  },
  
  // 切换月日历显示
  toggleMonthCalendar: function() {
    const showMonthCalendar = !this.data.showMonthCalendar;
    this.setData({
      showMonthCalendar
    });
  },
  
  // 上个月（月日历中使用）
  prevMonth: function() {
    const currentMonth = new Date(this.data.currentMonth);
    currentMonth.setMonth(currentMonth.getMonth() - 1);
    
    this.setData({
      currentMonth,
      currentYearMonth: `${currentMonth.getFullYear()}年${util.formatNumber(currentMonth.getMonth() + 1)}月`
    });
    
    this.generateMonthDays(currentMonth);
    
    // 获取这个月的记录日期
    this.fetchRecordDates(currentMonth.getFullYear(), currentMonth.getMonth() + 1);
  },
  
  // 下个月（月日历中使用）
  nextMonth: function() {
    const currentMonth = new Date(this.data.currentMonth);
    currentMonth.setMonth(currentMonth.getMonth() + 1);
    
    this.setData({
      currentMonth,
      currentYearMonth: `${currentMonth.getFullYear()}年${util.formatNumber(currentMonth.getMonth() + 1)}月`
    });
    
    this.generateMonthDays(currentMonth);
    
    // 获取这个月的记录日期
    this.fetchRecordDates(currentMonth.getFullYear(), currentMonth.getMonth() + 1);
  },
  
  // 生成月日历数据
  generateMonthDays: function(date) {
    const year = date.getFullYear();
    const month = date.getMonth();
    
    // 该月第一天
    const firstDay = new Date(year, month, 1);
    // 该月最后一天
    const lastDay = new Date(year, month + 1, 0);
    
    // 该月第一天是星期几
    const firstDayOfWeek = firstDay.getDay();
    
    const monthDays = [];
    const today = new Date();
    
    // 上个月需要显示的天数
    for (let i = 0; i < firstDayOfWeek; i++) {
      const prevDay = new Date(year, month, -i);
      monthDays.unshift({
        day: prevDay.getDate(),
        fullDate: util.formatDate(prevDay),
        isCurrentMonth: false,
        isToday: false
      });
    }
    
    // 当前月的天数
    for (let i = 1; i <= lastDay.getDate(); i++) {
      const currentDate = new Date(year, month, i);
      const isToday = 
        currentDate.getDate() === today.getDate() && 
        currentDate.getMonth() === today.getMonth() && 
        currentDate.getFullYear() === today.getFullYear();
      
      monthDays.push({
        day: i,
        fullDate: util.formatDate(currentDate),
        isCurrentMonth: true,
        isToday
      });
    }
    
    // 补齐下个月的天数
    const remainingDays = 7 - (monthDays.length % 7);
    if (remainingDays < 7) {
      for (let i = 1; i <= remainingDays; i++) {
        const nextDate = new Date(year, month + 1, i);
        monthDays.push({
          day: i,
          fullDate: util.formatDate(nextDate),
          isCurrentMonth: false,
          isToday: false
        });
      }
    }
    
    this.setData({ monthDays });
  },
  
  // 触摸开始事件
  calendarTouchStart: function(e) {
    this.setData({
      touchStartX: e.touches[0].clientX
    });
  },
  
  // 触摸移动事件
  calendarTouchMove: function(e) {
    this.setData({
      touchEndX: e.touches[0].clientX
    });
  },
  
  // 触摸结束事件
  calendarTouchEnd: function(e) {
    // 移除滑动切换日期功能，按用户要求取消特效
    return;
  },
  
  // 回到今天
  goToToday: function() {
    // 获取今天的日期
    const today = new Date();
    const todayFormatted = util.formatDate(today);
    
    // 更新当前选中日期和当前日期
    this.setData({
      selectedDate: todayFormatted,
      currentDate: todayFormatted,
      currentMonth: today,
      currentYearMonth: `${today.getFullYear()}年${util.formatNumber(today.getMonth() + 1)}月`
    });
    
    // 重新生成周视图和月视图
    this.generateWeekDays(today);
    this.generateMonthDays(today);
    
    // 加载对应日期的数据
    this.fetchFoodRecords(todayFormatted);
    this.fetchNutritionData(todayFormatted);
    this.fetchRecordDates(today.getFullYear(), today.getMonth() + 1);
  },
  
  // 重新计算营养百分比
  recalculateNutritionPercentages: function() {
    const nutrition = this.data.nutritionData;
    
    // 计算各个营养素的百分比，确保不为零
    const caloriesPercentage = Math.max(1, Math.round((nutrition.calories.current / nutrition.calories.target) * 100));
    const proteinPercentage = Math.max(1, Math.round((nutrition.protein.current / nutrition.protein.target) * 100));
    const fatPercentage = Math.max(1, Math.round((nutrition.fat.current / nutrition.fat.target) * 100));
    const carbsPercentage = Math.max(1, Math.round((nutrition.carbs.current / nutrition.carbs.target) * 100));
    
    // 移除百分比上限，允许超过100%
    this.setData({
      'nutritionData.calories.percentage': caloriesPercentage,
      'nutritionData.protein.percentage': proteinPercentage,
      'nutritionData.fat.percentage': fatPercentage,
      'nutritionData.carbs.percentage': carbsPercentage,
    });
  },

  // 生成一周日期数据
  generateWeekDays: function(currentDate) {
    const weekDays = [];
    const dayNames = ['日', '一', '二', '三', '四', '五', '六'];
    
    // 计算本周的开始日期（周日）
    const startOfWeek = new Date(currentDate);
    const day = currentDate.getDay(); // 0是周日，1是周一，以此类推
    startOfWeek.setDate(currentDate.getDate() - day);
    
    // 生成一周的日期
    for (let i = 0; i < 7; i++) {
      const date = new Date(startOfWeek);
      date.setDate(startOfWeek.getDate() + i);
      
      const formattedDate = util.formatDate(date);
      const today = new Date();
      
      weekDays.push({
        date: formattedDate,
        day: dayNames[i],
        number: date.getDate(),
        isToday: date.getDate() === today.getDate() && 
                date.getMonth() === today.getMonth() && 
                date.getFullYear() === today.getFullYear()
      });
    }
    
    this.setData({ weekDays });
  },

  // 从服务器获取有记录的日期
  fetchRecordDates: function(year, month) {
    // 获取token（如果有）
    const token = wx.getStorageSync('token');
    const header = {
      'Content-Type': 'application/json'
    };
    
    // 如果有token，添加到请求头
    if (token) {
      header['Authorization'] = `Bearer ${token}`;
    }
    
    wx.request({
      url: `${app.globalData.baseUrl}/api/record/getRecordDates`,
      method: 'GET',
      header: header,
      data: {
        year: year,
        month: month
      },
      success: (res) => {
        if (res.data.code === 0) {
          const recordDates = res.data.data.recordDates;
          
          // 更新周视图和月视图中的记录标记
          const weekDays = this.data.weekDays.map(day => {
            const date = new Date(day.date.replace(/年|月/g, '/').replace('日', ''));
            const hasRecord = date.getFullYear() === year && 
                              date.getMonth() + 1 === month && 
                              recordDates.includes(date.getDate());
            return {
              ...day,
              hasRecord
            };
          });
          
          const monthDays = this.data.monthDays.map(day => {
            const hasRecord = day.isCurrentMonth && recordDates.includes(day.day);
            return {
              ...day,
              hasRecord
            };
          });
          
          this.setData({
            weekDays,
            monthDays
          });
        } else {
          console.error('获取记录日期失败:', res.data.message);
        }
      },
      fail: (err) => {
        console.error('获取记录日期请求失败:', err);
      }
    });
  },
  
  // 从服务器获取食物记录
  fetchFoodRecords: function(date) {
    // 获取token（如果有）
    const token = wx.getStorageSync('token');
    const header = {
      'Content-Type': 'application/json'
    };
    
    // 如果有token，添加到请求头
    if (token) {
      header['Authorization'] = `Bearer ${token}`;
    }
    
    // 将date转换为YYYY-MM-DD格式
    const dateStr = date.replace(/年|月|日/g, (match) => {
      if (match === '年') return '-';
      if (match === '月') return '-';
      return '';
    });
    
    wx.request({
      url: `${app.globalData.baseUrl}/api/record/getByDate`,
      method: 'GET',
      header: header,
      data: {
        date: dateStr
      },
      success: (res) => {
        if (res.data.code === 0) {
          const foodRecords = res.data.data.foodRecords || [];
          this.setData({ foodRecords });
          
          // 检查是否有晚餐记录
          this.checkHasDinner();
        } else {
          console.error('获取食物记录失败:', res.data.message);
          // 清空记录
          this.setData({ foodRecords: [] });
        }
      },
      fail: (err) => {
        console.error('获取食物记录请求失败:', err);
        // 请求失败时清空记录
        this.setData({ foodRecords: [] });
      }
    });
  },
  
  // 从服务器获取营养数据
  fetchNutritionData: function(date) {
    // 获取token（如果有）
    const token = wx.getStorageSync('token');
    const header = {
      'Content-Type': 'application/json'
    };
    
    // 如果有token，添加到请求头
    if (token) {
      header['Authorization'] = `Bearer ${token}`;
    }
    
    // 将date转换为YYYY-MM-DD格式
    const dateStr = date.replace(/年|月|日/g, (match) => {
      if (match === '年') return '-';
      if (match === '月') return '-';
      return '';
    });
    
    wx.request({
      url: `${app.globalData.baseUrl}/api/record/getNutrition`,
      method: 'GET',
      header: header,
      data: {
        date: dateStr
      },
      success: (res) => {
        if (res.data.code === 0) {
          const nutritionData = res.data.data.nutritionData;
          this.setData({ nutritionData });
        } else {
          console.error('获取营养数据失败:', res.data.message);
        }
      },
      fail: (err) => {
        console.error('获取营养数据请求失败:', err);
      }
    });
  },
  
  // 提交食物记录
  submitFoodRecord: function() {
    // 验证输入
    const newFood = this.data.newFood;
    if (!newFood.name || !newFood.calories || !newFood.protein || !newFood.fat || !newFood.carbs) {
      wx.showToast({
        title: '请填写完整的食物信息',
        icon: 'none'
      });
      return;
    }
    
    // 获取token（如果有）
    const token = wx.getStorageSync('token');
    const header = {
      'Content-Type': 'application/json'
    };
    
    // 如果有token，添加到请求头
    if (token) {
      header['Authorization'] = `Bearer ${token}`;
    }
    
    // 准备请求数据
    const recordData = {
      date: this.data.selectedDate.replace(/年|月|日/g, (match) => {
        if (match === '年') return '-';
        if (match === '月') return '-';
        return '';
      }),
      mealType: this.data.mealTypes[this.data.mealTypeIndex],
      mealTime: this.data.mealTime,
      food: {
        name: newFood.name,
        calories: parseFloat(newFood.calories),
        protein: parseFloat(newFood.protein),
        fat: parseFloat(newFood.fat),
        carbs: parseFloat(newFood.carbs)
      }
    };
    
    // 如果是编辑模式，调用更新接口
    if (this.data.editingFoodInfo) {
      recordData.recordId = this.data.editingFoodInfo.recordId;
      
      wx.request({
        url: `${app.globalData.baseUrl}/api/record/update`,
        method: 'PUT',
        header: header,
        data: recordData,
        success: (res) => {
          if (res.data.code === 0) {
            wx.showToast({
              title: '更新成功',
              icon: 'success'
            });
            this.hideAddFoodRecord();
            // 刷新食物记录
            this.fetchFoodRecords(this.data.selectedDate);
            this.fetchNutritionData(this.data.selectedDate);
          } else {
            wx.showToast({
              title: res.data.message || '更新失败',
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          wx.showToast({
            title: '网络请求失败',
            icon: 'none'
          });
        }
      });
    } else {
      // 新增记录
      wx.request({
        url: `${app.globalData.baseUrl}/api/record/add`,
        method: 'POST',
        header: header,
        data: recordData,
        success: (res) => {
          if (res.data.code === 0) {
            wx.showToast({
              title: '添加成功',
              icon: 'success'
            });
            this.hideAddFoodRecord();
            // 刷新食物记录
            this.fetchFoodRecords(this.data.selectedDate);
            this.fetchNutritionData(this.data.selectedDate);
          } else {
            wx.showToast({
              title: res.data.message || '添加失败',
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          wx.showToast({
            title: '网络请求失败',
            icon: 'none'
          });
        }
      });
    }
  },
  
  // 删除食物记录
  deleteFoodRecord: function(e) {
    const recordId = e.currentTarget.dataset.recordid;
    if (!recordId) {
      wx.showToast({
        title: '记录ID不能为空',
        icon: 'none'
      });
      return;
    }
    
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这条食物记录吗？',
      success: (res) => {
        if (res.confirm) {
          // 获取token（如果有）
          const token = wx.getStorageSync('token');
          const header = {
            'Content-Type': 'application/json'
          };
          
          // 如果有token，添加到请求头
          if (token) {
            header['Authorization'] = `Bearer ${token}`;
          }
          
          wx.request({
            url: `${app.globalData.baseUrl}/api/record/delete`,
            method: 'DELETE',
            header: header,
            data: {
              recordId: recordId
            },
            success: (res) => {
              if (res.data.code === 0) {
                wx.showToast({
                  title: '删除成功',
                  icon: 'success'
                });
                // 刷新食物记录
                this.fetchFoodRecords(this.data.selectedDate);
                this.fetchNutritionData(this.data.selectedDate);
              } else {
                wx.showToast({
                  title: res.data.message || '删除失败',
                  icon: 'none'
                });
              }
            },
            fail: (err) => {
              wx.showToast({
                title: '网络请求失败',
                icon: 'none'
              });
            }
          });
        }
      }
    });
  },

  // 切换编辑模式
  toggleEditMode: function() {
    this.setData({
      isEditMode: !this.data.isEditMode
    });
  },
  
  // 食物条目点击
  foodItemTap: function(e) {
    // 如果在编辑模式下，点击不执行任何操作
    if (this.data.isEditMode) {
      return;
    }
    
    // 在非编辑模式下，可以添加食物点击后的详情查看等功能
  },
  
  // 记录拖拽开始位置
  dragStart: function(e) {
    if (!this.data.isEditMode) return;
    
    const mealIndex = e.currentTarget.dataset.mealIndex;
    const foodIndex = e.currentTarget.dataset.foodIndex;
    
    this.setData({
      dragMealIndex: mealIndex,
      dragFoodIndex: foodIndex,
      isDragging: true,
      startY: e.changedTouches[0].clientY
    });
  },
  
  // 记录拖拽移动
  dragMove: function(e) {
    if (!this.data.isEditMode || !this.data.isDragging) return;
    
    // 拖拽逻辑将在后续开发中完善
    // 目前只做状态标记，不实际移动元素
  },
  
  // 记录拖拽结束
  dragEnd: function(e) {
    if (!this.data.isEditMode) return;
    
    this.setData({
      isDragging: false,
      dragMealIndex: -1,
      dragFoodIndex: -1
    });
    
    // 拖拽结束后的处理逻辑将在后续开发中完善
  },
  
  // 阻止滚动穿透
  catchTouchMove: function() {
    return false;
  },

  // 编辑食物记录
  editFoodRecord: function(e) {
    const index = e.currentTarget.dataset.index;
    const foodIndex = e.currentTarget.dataset.foodindex;
    const mealType = this.data.foodRecords[index].mealType;
    const food = this.data.foodRecords[index].foods[foodIndex];
    
    // 查找餐次索引
    const mealTypeIndex = this.data.mealTypes.findIndex(type => type === mealType);
    
    this.setData({
      showAddModal: true,
      mealTypeIndex: mealTypeIndex !== -1 ? mealTypeIndex : 0,
      mealTime: this.data.foodRecords[index].mealTime || '12:00',
      newFood: {
        name: food.name,
        calories: food.calories.toString(),
        protein: food.protein.toString(),
        fat: food.fat.toString(),
        carbs: food.carbs.toString()
      },
      editingFoodInfo: {
        recordId: food.recordId,
        index,
        foodIndex
      }
    });
  },
})
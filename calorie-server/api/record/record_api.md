# 食物记录API接口设计

## 1. 用户日常记录接口

### 1.1 添加食物记录
- 路径: `/api/record/add`
- 方法: `POST`
- 描述: 添加用户单条食物记录
- 请求参数:
  ```json
  {
    "userId": "用户ID",
    "date": "2023-04-05", 
    "mealType": "早餐|午餐|下午茶|晚餐|夜宵",
    "mealTime": "08:30",
    "food": {
      "name": "食物名称",
      "quantity": "数量描述(可选)",
      "calories": 150,
      "protein": 10,
      "fat": 5,
      "carbs": 20
    }
  }
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "添加成功",
    "data": {
      "recordId": "记录ID"
    }
  }
  ```

### 1.2 批量添加食物记录
- 路径: `/api/record/batchAdd`
- 方法: `POST`
- 描述: 批量添加食物记录
- 请求参数:
  ```json
  {
    "userId": "用户ID",
    "date": "2023-04-05",
    "mealType": "早餐|午餐|下午茶|晚餐|夜宵",
    "mealTime": "08:30",
    "foods": [
      {
        "name": "食物1",
        "quantity": "数量描述(可选)",
        "calories": 150,
        "protein": 10,
        "fat": 5,
        "carbs": 20
      },
      {
        "name": "食物2",
        "quantity": "数量描述(可选)",
        "calories": 200,
        "protein": 15,
        "fat": 8,
        "carbs": 25
      }
    ]
  }
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "添加成功",
    "data": {
      "recordIds": ["记录ID1", "记录ID2"]
    }
  }
  ```

### 1.3 更新食物记录
- 路径: `/api/record/update`
- 方法: `PUT`
- 描述: 更新食物记录
- 请求参数:
  ```json
  {
    "recordId": "记录ID",
    "mealType": "早餐|午餐|下午茶|晚餐|夜宵(可选)",
    "mealTime": "08:30(可选)",
    "food": {
      "name": "食物名称(可选)",
      "quantity": "数量描述(可选)",
      "calories": 150,
      "protein": 10,
      "fat": 5,
      "carbs": 20
    }
  }
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "更新成功"
  }
  ```

### 1.4 删除食物记录
- 路径: `/api/record/delete`
- 方法: `DELETE`
- 描述: 删除食物记录
- 请求参数:
  ```json
  {
    "recordId": "记录ID"
  }
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "删除成功"
  }
  ```

### 1.5 获取日期食物记录
- 路径: `/api/record/getByDate`
- 方法: `GET`
- 描述: 获取指定日期的所有食物记录
- 请求参数:
  ```
  userId=用户ID&date=2023-04-05
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "获取成功",
    "data": {
      "date": "2023-04-05",
      "foodRecords": [
        {
          "mealType": "早餐",
          "mealTime": "08:00",
          "foods": [
            {
              "recordId": "记录ID1",
              "name": "全麦面包",
              "quantity": "2片",
              "calories": 160,
              "protein": 8,
              "fat": 2,
              "carbs": 30
            },
            {
              "recordId": "记录ID2",
              "name": "煮鸡蛋",
              "quantity": "2个",
              "calories": 140,
              "protein": 12,
              "fat": 10,
              "carbs": 0
            }
          ]
        },
        {
          "mealType": "午餐",
          "mealTime": "12:30",
          "foods": [
            {
              "recordId": "记录ID3",
              "name": "烤鸡沙拉",
              "quantity": "",
              "calories": 300,
              "protein": 25,
              "fat": 10,
              "carbs": 30
            }
          ]
        }
      ]
    }
  }
  ```

### 1.6 获取用户营养摄入统计
- 路径: `/api/record/getNutrition`
- 方法: `GET`
- 描述: 获取用户指定日期的营养摄入统计
- 请求参数:
  ```
  userId=用户ID&date=2023-04-05
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "获取成功",
    "data": {
      "date": "2023-04-05",
      "nutritionData": {
        "calories": {
          "current": 1200,
          "target": 2000,
          "percentage": 60,
          "remaining": 800
        },
        "protein": {
          "current": 62,
          "target": 125,
          "percentage": 50
        },
        "fat": {
          "current": 50,
          "target": 83,
          "percentage": 60
        },
        "carbs": {
          "current": 156,
          "target": 313,
          "percentage": 50
        }
      }
    }
  }
  ```

### 1.7 获取日期记录状态
- 路径: `/api/record/getRecordDates`
- 方法: `GET`
- 描述: 获取指定月份哪些日期有记录
- 请求参数:
  ```
  userId=用户ID&year=2023&month=4
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "获取成功",
    "data": {
      "year": 2023,
      "month": 4,
      "recordDates": [1, 3, 5, 10, 15, 20]
    }
  }
  ```

## 2. 食物库接口

### 2.1 搜索食物
- 路径: `/api/food/search`
- 方法: `GET`
- 描述: 搜索食物库
- 请求参数:
  ```
  keyword=面包&page=1&pageSize=10
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "搜索成功",
    "data": {
      "total": 156,
      "foods": [
        {
          "foodId": "食物ID1",
          "name": "全麦面包",
          "calories": 160,
          "protein": 8,
          "fat": 2,
          "carbs": 30,
          "unit": "片",
          "unitWeight": 40
        },
        {
          "foodId": "食物ID2",
          "name": "法棍面包",
          "calories": 180,
          "protein": 6,
          "fat": 1,
          "carbs": 38,
          "unit": "根",
          "unitWeight": 60
        }
      ]
    }
  }
  ```

### 2.2 获取推荐食物
- 路径: `/api/food/recommend`
- 方法: `GET`
- 描述: 获取推荐食物列表
- 请求参数:
  ```
  userId=用户ID&mealType=早餐&page=1&pageSize=10
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "获取成功",
    "data": {
      "foods": [
        {
          "foodId": "食物ID1",
          "name": "全麦面包",
          "calories": 160,
          "protein": 8,
          "fat": 2,
          "carbs": 30,
          "unit": "片",
          "unitWeight": 40
        },
        {
          "foodId": "食物ID2",
          "name": "脱脂牛奶",
          "calories": 90,
          "protein": 9,
          "fat": 0,
          "carbs": 12,
          "unit": "杯",
          "unitWeight": 240
        }
      ]
    }
  }
  ```

## 3. 用户营养目标接口

### 3.1 获取用户营养目标
- 路径: `/api/user/nutritionTarget`
- 方法: `GET`
- 描述: 获取用户的营养目标设置
- 请求参数:
  ```
  userId=用户ID
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "获取成功",
    "data": {
      "calories": 2000,
      "protein": 125,
      "fat": 83,
      "carbs": 313
    }
  }
  ```

### 3.2 更新用户营养目标
- 路径: `/api/user/updateNutritionTarget`
- 方法: `PUT`
- 描述: 更新用户的营养目标设置
- 请求参数:
  ```json
  {
    "userId": "用户ID",
    "calories": 2000,
    "protein": 125,
    "fat": 83,
    "carbs": 313
  }
  ```
- 返回:
  ```json
  {
    "code": 0,
    "message": "更新成功"
  }
  ```
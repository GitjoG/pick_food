-- Active: 1743669286511@@127.0.0.1@3306
-- 用户表
create database if not exists calorie_custom;
use calorie_custom

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    openid VARCHAR(100) UNIQUE NOT NULL COMMENT '微信用户唯一标识',
    username VARCHAR(50) COMMENT '用户名',
    phone VARCHAR(20) COMMENT '手机号',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 用户信息表
CREATE TABLE user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '关联用户ID',
    height DECIMAL(5,2) COMMENT '身高(cm)',
    weight DECIMAL(5,2) COMMENT '体重(kg)',
    age INT COMMENT '年龄',
    gender ENUM('male', 'female', 'other') COMMENT '性别',
    activity_level ENUM('sedentary', 'light', 'moderate', 'active', 'very_active') COMMENT '活动量级别',
    bmr DECIMAL(8,2) COMMENT '基础代谢率',
    tdee DECIMAL(8,2) COMMENT '总能量消耗',
    calorie_target DECIMAL(8,2) COMMENT '目标热量',
    protein_target DECIMAL(6,2) COMMENT '蛋白质目标(g)',
    fat_target DECIMAL(6,2) COMMENT '脂肪目标(g)',
    carb_target DECIMAL(6,2) COMMENT '碳水目标(g)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';

-- 餐厅表
CREATE TABLE restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '餐厅名称',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='餐厅表';

-- 菜品表
CREATE TABLE food_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL COMMENT '关联餐厅ID',
    name VARCHAR(100) NOT NULL COMMENT '菜品名称',
    calories DECIMAL(8,2) NOT NULL COMMENT '热量(千卡)',
    protein DECIMAL(6,2) NOT NULL COMMENT '蛋白质(g)',
    fat DECIMAL(6,2) NOT NULL COMMENT '脂肪(g)',
    carbs DECIMAL(6,2) NOT NULL COMMENT '碳水化合物(g)',
    image_url VARCHAR(255) COMMENT '菜品图片URL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='菜品表';

-- 食物记录表
CREATE TABLE food_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '关联用户ID',
    food_item_id INT COMMENT '关联菜品ID(可为空，自定义食物时)',
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL COMMENT '餐次类型',
    custom_food_name VARCHAR(100) COMMENT '自定义食物名称',
    calories DECIMAL(8,2) NOT NULL COMMENT '热量(千卡)',
    protein DECIMAL(6,2) NOT NULL COMMENT '蛋白质(g)',
    fat DECIMAL(6,2) NOT NULL COMMENT '脂肪(g)',
    carbs DECIMAL(6,2) NOT NULL COMMENT '碳水化合物(g)',
    record_date DATE NOT NULL COMMENT '记录日期',
    record_time TIME NOT NULL COMMENT '记录时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_item_id) REFERENCES food_items(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='食物记录表';

-- 用户反馈表
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `openid` varchar(100) NOT NULL COMMENT '微信用户唯一标识',
  `username` varchar(50) DEFAULT NULL COMMENT '用户名',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `nickname` varchar(255) DEFAULT NULL,
  `avatar_url` varchar(255) DEFAULT NULL,
  `session_key` varchar(255) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `openid` (`openid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表'
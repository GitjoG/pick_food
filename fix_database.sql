-- 修复数据库表结构
USE calorie_custom;

-- 修复users表，添加缺失的字段
ALTER TABLE users
ADD COLUMN nickname VARCHAR(255) COMMENT '微信昵称' AFTER phone,
ADD COLUMN avatar_url VARCHAR(255) COMMENT '头像URL' AFTER nickname,
ADD COLUMN session_key VARCHAR(255) COMMENT '会话密钥' AFTER avatar_url,
ADD COLUMN last_login DATETIME COMMENT '最后登录时间' AFTER session_key;

-- 创建缺失的食物分类表
CREATE TABLE IF NOT EXISTS food_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE COMMENT '分类名称',
    description TEXT COMMENT '分类描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='食物分类表';

-- 创建缺失的食物与分类关联表
CREATE TABLE IF NOT EXISTS food_category_association (
    food_id INT NOT NULL COMMENT '食物ID',
    category_id INT NOT NULL COMMENT '分类ID',
    PRIMARY KEY (food_id, category_id),
    FOREIGN KEY (food_id) REFERENCES food_items(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES food_categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='食物与分类关联表';

-- 创建缺失的用户反馈表
CREATE TABLE IF NOT EXISTS user_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    content TEXT NOT NULL COMMENT '反馈内容',
    status ENUM('pending', 'processing', 'resolved') DEFAULT 'pending' COMMENT '处理状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户反馈表'; 
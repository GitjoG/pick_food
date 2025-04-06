#!/bin/bash

# 启动后端
cd backend
python3 -m flask run --host=0.0.0.0 --port=5000 &

# 启动前端
cd ../frontend
npm run serve &

echo "后台管理系统已启动"
echo "后端API地址: http://localhost:5000"
echo "前端页面地址: http://localhost:8080" 
#!/bin/bash

BASE_URL="http://localhost:4000/api/user"

# 假设有一个测试用户ID
TEST_USER_ID=1

echo "测试计算BMR接口并保存到数据库..."
curl -s -X POST $BASE_URL/calculateBMR \
  -H "Content-Type: application/json" \
  -d "{\"weight\": 70, \"height\": 175, \"age\": 30, \"gender\": \"male\", \"user_id\": $TEST_USER_ID}" | json_pp

echo -e "\n\n测试计算TDEE接口并保存到数据库..."
curl -s -X POST $BASE_URL/calculateTDEE \
  -H "Content-Type: application/json" \
  -d "{\"bmr\": 1655, \"activity_level\": \"moderate\", \"user_id\": $TEST_USER_ID}" | json_pp

echo -e "\n\n测试计算营养素需求接口并保存到数据库..."
curl -s -X POST $BASE_URL/calculateNutrients \
  -H "Content-Type: application/json" \
  -d "{\"tdee\": 2565, \"goal\": \"lose\", \"user_id\": $TEST_USER_ID}" | json_pp

echo -e "\n\n测试计算热量需求和缺口接口并保存到数据库..."
curl -s -X POST $BASE_URL/calculateCalorie \
  -H "Content-Type: application/json" \
  -d "{\"tdee\": 2565, \"current_intake\": 2000, \"goal\": \"maintain\", \"user_id\": $TEST_USER_ID}" | json_pp

echo -e "\n\n测试一体化计算接口并保存到数据库..."
curl -s -X POST $BASE_URL/calculateAll \
  -H "Content-Type: application/json" \
  -d "{\"weight\": 70, \"height\": 175, \"age\": 30, \"gender\": \"male\", \"activity_level\": \"moderate\", \"goal\": \"maintain\", \"current_intake\": 2000, \"user_id\": $TEST_USER_ID}" | json_pp

echo -e "\n\n测试获取用户信息..."
curl -s -X GET "$BASE_URL/info?user_id=$TEST_USER_ID" | json_pp

echo -e "\n\n测试更新用户信息..."
curl -s -X PUT $BASE_URL/info \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": $TEST_USER_ID, \"username\": \"测试用户\", \"height\": 180}" | json_pp

echo -e "\n\n测试获取用户设置..."
curl -s -X GET "$BASE_URL/settings?user_id=$TEST_USER_ID" | json_pp

echo -e "\n\n测试更新用户设置..."
curl -s -X PUT $BASE_URL/settings \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": $TEST_USER_ID, \"calorie_target\": 2200}" | json_pp

echo -e "\n\n测试提交用户反馈..."
curl -s -X POST $BASE_URL/feedback \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": $TEST_USER_ID, \"feedback_type\": \"suggestion\", \"content\": \"希望能增加更多食物选择\"}" | json_pp

echo -e "\n\n测试错误处理..."
curl -s -X POST $BASE_URL/calculateBMR \
  -H "Content-Type: application/json" \
  -d '{"weight": 70, "height": 175}' | json_pp 
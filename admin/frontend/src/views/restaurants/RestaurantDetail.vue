<template>
  <div class="restaurant-detail">
    <h1>餐厅详情</h1>
    
    <el-card class="detail-card">
      <el-descriptions title="基本信息" :column="2" border>
        <el-descriptions-item label="餐厅名称">{{ restaurant.name }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ restaurant.created_at }}</el-descriptions-item>
        <el-descriptions-item label="菜品数量">{{ restaurant.food_count }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="menu-card">
      <div slot="header">
        <span>菜单管理</span>
        <el-button 
          style="float: right; padding: 3px 0" 
          type="text"
          @click="handleAddFood"
        >添加菜品</el-button>
      </div>
      
      <el-table :data="menuItems" style="width: 100%">
        <el-table-column prop="name" label="菜品名称"></el-table-column>
        <el-table-column prop="calories" label="热量(kcal)"></el-table-column>
        <el-table-column prop="protein" label="蛋白质(g)"></el-table-column>
        <el-table-column prop="fat" label="脂肪(g)"></el-table-column>
        <el-table-column prop="carbs" label="碳水(g)"></el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <el-button 
              size="mini" 
              type="primary" 
              @click="handleEditFood(scope.row)"
            >编辑</el-button>
            <el-button 
              size="mini" 
              type="danger" 
              @click="handleDeleteFood(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑菜品对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible">
      <el-form :model="foodForm" label-width="100px">
        <el-form-item label="菜品名称">
          <el-input v-model="foodForm.name"></el-input>
        </el-form-item>
        <el-form-item label="热量(kcal)">
          <el-input-number v-model="foodForm.calories" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="蛋白质(g)">
          <el-input-number v-model="foodForm.protein" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="脂肪(g)">
          <el-input-number v-model="foodForm.fat" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="碳水(g)">
          <el-input-number v-model="foodForm.carbs" :min="0"></el-input-number>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmitFood">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RestaurantDetail',
  data() {
    return {
      restaurantId: this.$route.params.id,
      restaurant: {},
      menuItems: [],
      dialogVisible: false,
      dialogTitle: '添加菜品',
      foodForm: {
        name: '',
        calories: 0,
        protein: 0,
        fat: 0,
        carbs: 0
      }
    }
  },
  created() {
    this.fetchRestaurantInfo()
    this.fetchMenuItems()
  },
  methods: {
    async fetchRestaurantInfo() {
      try {
        const response = await axios.get(`/restaurants/${this.restaurantId}`)
        this.restaurant = response.data
      } catch (error) {
        console.error('获取餐厅信息失败:', error)
        this.$message.error('获取餐厅信息失败')
        
        // Fallback to mock data
        this.restaurant = {
          id: this.restaurantId,
          name: '示例餐厅',
          created_at: '2023-01-01',
          food_count: 2
        }
      }
    },
    async fetchMenuItems() {
      try {
        const response = await axios.get(`/restaurants/${this.restaurantId}/menu`)
        this.menuItems = response.data || []
      } catch (error) {
        console.error('获取菜单失败:', error)
        this.$message.error('获取菜单失败')
        
        // Fallback to mock data
        this.menuItems = [
          {
            id: 1,
            name: '示例菜品1',
            calories: 200,
            protein: 10,
            fat: 5,
            carbs: 30
          },
          {
            id: 2,
            name: '示例菜品2',
            calories: 300,
            protein: 15,
            fat: 8,
            carbs: 40
          }
        ]
      }
    },
    handleAddFood() {
      this.dialogTitle = '添加菜品'
      this.foodForm = {
        name: '',
        calories: 0,
        protein: 0,
        fat: 0,
        carbs: 0
      }
      this.dialogVisible = true
    },
    handleEditFood(row) {
      this.dialogTitle = '编辑菜品'
      this.foodForm = { ...row }
      this.dialogVisible = true
    },
    async handleDeleteFood(row) {
      try {
        await this.$confirm('确认删除该菜品?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await axios.delete(`/restaurants/${this.restaurantId}/menu/${row.id}`)
        this.$message.success('删除成功')
        this.fetchMenuItems()
        this.fetchRestaurantInfo() // Update food count
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除菜品失败:', error)
          this.$message.error('删除失败: ' + (error.response?.data?.message || error.message))
        }
      }
    },
    async handleSubmitFood() {
      try {
        if (this.foodForm.id) {
          // Update existing food item
          await axios.put(`/restaurants/${this.restaurantId}/menu/${this.foodForm.id}`, this.foodForm)
          this.$message.success('菜品更新成功')
        } else {
          // Create new food item
          await axios.post(`/restaurants/${this.restaurantId}/menu`, this.foodForm)
          this.$message.success('菜品添加成功')
        }
        this.dialogVisible = false
        this.fetchMenuItems() // Refresh the menu
        this.fetchRestaurantInfo() // Update food count
      } catch (error) {
        console.error('保存菜品失败:', error)
        this.$message.error('保存菜品失败: ' + (error.response?.data?.message || error.message))
      }
    }
  }
}
</script>

<style scoped>
.restaurant-detail {
  padding: 20px;
}
.detail-card {
  margin-bottom: 20px;
}
.menu-card {
  margin-top: 20px;
}
</style> 
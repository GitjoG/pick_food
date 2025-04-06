<template>
  <div class="restaurant-list">
    <div class="page-header">
      <h1>餐厅列表</h1>
      <el-button type="primary" @click="handleAdd">添加餐厅</el-button>
    </div>

    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索餐厅"
        style="width: 200px"
        @input="handleSearch"
      >
        <i slot="prefix" class="el-icon-search"></i>
      </el-input>
    </div>
    
    <el-table :data="restaurants" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="name" label="餐厅名称"></el-table-column>
      <el-table-column prop="food_count" label="菜品数量"></el-table-column>
      <el-table-column prop="created_at" label="创建时间"></el-table-column>
      <el-table-column label="操作" width="300">
        <template slot-scope="scope">
          <el-button 
            size="mini" 
            @click="handleView(scope.row)"
          >查看</el-button>
          <el-button 
            size="mini"
            type="success" 
            @click="handleMenu(scope.row)"
          >菜单</el-button>
          <el-button 
            size="mini" 
            type="primary" 
            @click="handleEdit(scope.row)"
          >编辑</el-button>
          <el-button 
            size="mini" 
            type="danger" 
            @click="handleDelete(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </div>

    <!-- 添加/编辑餐厅对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible">
      <el-form :model="restaurantForm" label-width="100px">
        <el-form-item label="餐厅名称">
          <el-input v-model="restaurantForm.name"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RestaurantList',
  data() {
    return {
      restaurants: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      total: 0,
      dialogVisible: false,
      dialogTitle: '添加餐厅',
      restaurantForm: {
        name: '',
       
      }
    }
  },
  created() {
    this.fetchRestaurants()
  },
  methods: {
    async fetchRestaurants() {
      try {
        // Get restaurants from the backend
        const response = await axios.get('/restaurants/list', {
          params: {
            page: this.currentPage,
            per_page: this.pageSize,
            search: this.searchQuery
          }
        })
        
        this.restaurants = response.data.items || []
        this.total = response.data.total || 0
      } catch (error) {
        console.error('获取餐厅列表失败:', error)
        this.$message.error('获取餐厅列表失败')
        
        // Fallback to mock data if API fails
        this.restaurants = [
          {
            id: 1,
            name: '示例餐厅1',
          
            food_count: 5,
            created_at: '2023-01-01 12:00:00'
          },
          {
            id: 2,
            name: '示例餐厅2',
           
            food_count: 8,
            created_at: '2023-01-02 12:00:00'
          }
        ]
        this.total = this.restaurants.length
      }
    },
    handleAdd() {
      this.dialogTitle = '添加餐厅'
      this.restaurantForm = {
        name: ''
       
      }
      this.dialogVisible = true
    },
    handleView(row) {
      this.$router.push(`/restaurants/${row.id}`)
    },
    handleMenu(row) {
      this.$router.push(`/restaurants/${row.id}/menu`)
    },
    handleEdit(row) {
      this.dialogTitle = '编辑餐厅'
      this.restaurantForm = { ...row }
      this.dialogVisible = true
    },
    async handleDelete(row) {
      try {
        await this.$confirm('确认删除该餐厅?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await axios.delete(`/restaurants/${row.id}`)
        this.$message.success('删除成功')
        this.fetchRestaurants()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除餐厅失败:', error)
          this.$message.error('删除失败: ' + (error.response?.data?.message || error.message))
        }
      }
    },
    async handleSubmit() {
      try {
        if (this.restaurantForm.id) {
          // Update existing restaurant
          await axios.put(`/restaurants/${this.restaurantForm.id}`, this.restaurantForm)
          this.$message.success('餐厅更新成功')
        } else {
          // Create new restaurant
          await axios.post('/restaurants', this.restaurantForm)
          this.$message.success('餐厅添加成功')
        }
        this.dialogVisible = false
        this.fetchRestaurants() // Refresh the list
      } catch (error) {
        console.error('保存餐厅失败:', error)
        this.$message.error('保存餐厅失败: ' + (error.response?.data?.message || error.message))
      }
    },
    handleSearch() {
      this.currentPage = 1
      this.fetchRestaurants()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.fetchRestaurants()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchRestaurants()
    }
  }
}
</script>

<style scoped>
.restaurant-list {
  padding: 20px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.search-bar {
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 
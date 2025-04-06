<template>
  <div class="user-list">
    <h1>用户列表</h1>
    <div class="table-operations">
      <el-input
        v-model="searchQuery"
        placeholder="搜索用户"
        style="width: 200px"
        @input="handleSearch"
      >
        <i slot="prefix" class="el-icon-search"></i>
      </el-input>
    </div>
    
    <el-table :data="users" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="username" label="用户名"></el-table-column>
      <el-table-column prop="phone" label="手机号"></el-table-column>
      <el-table-column prop="created_at" label="创建时间"></el-table-column>
      <el-table-column label="操作" width="250">
        <template slot-scope="scope">
          <el-button 
            size="mini" 
            @click="handleView(scope.row)"
          >查看</el-button>
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
  </div>
</template>

<script>
export default {
  name: 'UserList',
  data() {
    return {
      users: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      total: 0
    }
  },
  created() {
    this.fetchUsers()
  },
  methods: {
    fetchUsers() {
      // 模拟数据
      this.users = [
        {
          id: 1,
          username: '测试用户1',
          phone: '13800138001',
          created_at: '2023-01-01'
        },
        {
          id: 2,
          username: '测试用户2',
          phone: '13800138002',
          created_at: '2023-01-02'
        }
      ]
      this.total = 2
    },
    handleView(row) {
      this.$router.push(`/users/${row.id}`)
    },
    handleEdit(row) {
      console.log('Edit:', row)
    },
    handleDelete(row) {
      this.$confirm('确认删除该用户?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log('Delete:', row)
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {})
    },
    handleSearch() {
      this.currentPage = 1
      this.fetchUsers()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.fetchUsers()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchUsers()
    }
  }
}
</script>

<style scoped>
.table-operations {
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 
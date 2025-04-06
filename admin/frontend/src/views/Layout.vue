<template>
  <el-container class="app-container">
    <el-aside width="200px" class="sidebar-container">
      <div class="logo">
        <!-- 暂时注释掉 logo 图片 -->
        <!-- <img src="../assets/logo.png" alt="Logo" height="40"> -->
        <span>热量定制管理</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item index="/dashboard">
          <i class="el-icon-s-home"></i>
          <span slot="title">仪表盘</span>
        </el-menu-item>
        
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-user"></i>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/users">用户列表</el-menu-item>
        </el-submenu>

        <!-- 添加餐厅管理菜单 -->
        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-shop"></i>
            <span>餐厅管理</span>
          </template>
          <el-menu-item index="/restaurants">餐厅列表</el-menu-item>
        </el-submenu>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="app-header">
        <div class="header-left">
          <i class="el-icon-menu toggle-sidebar" @click="toggleSidebar"></i>
          <breadcrumb />
        </div>
        <div class="header-right">
          <el-dropdown trigger="click">
            <span class="user-dropdown">
              {{ adminName }} <i class="el-icon-arrow-down"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人信息</el-dropdown-item>
              <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import Breadcrumb from '@/components/common/Breadcrumb'
import { getAdminName, logout } from '@/utils/auth'

export default {
  name: 'Layout',
  components: {
    Breadcrumb
  },
  data() {
    return {
      adminName: getAdminName()
    }
  },
  computed: {
    activeMenu() {
      const { path } = this.$route
      return path
    }
  },
  methods: {
    toggleSidebar() {
      // 实现侧边栏折叠功能
    },
    logout() {
      logout()
    }
  }
}
</script>

<style scoped>
.app-container {
  height: 100%;
}

.sidebar-container {
  background-color: #304156;
  height: 100%;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b2f3a;
  color: #fff;
}

.logo span {
  margin-left: 10px;
  font-size: 16px;
  font-weight: bold;
}

.sidebar-menu {
  border-right: none;
}

.app-header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-sidebar {
  font-size: 20px;
  cursor: pointer;
  margin-right: 20px;
}

.user-dropdown {
  cursor: pointer;
  color: #606266;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style> 
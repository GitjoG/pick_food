import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/views/Login'
import Layout from '@/views/Layout'
import Dashboard from '@/views/Dashboard'
import UserList from '@/views/users/UserList'
import UserDetail from '@/views/users/UserDetail'
import RestaurantList from '@/views/restaurants/RestaurantList'
import RestaurantDetail from '@/views/restaurants/RestaurantDetail'
import Register from '@/views/Register'
import { isLoggedIn } from '@/utils/auth'

// 删除所有其他未实现组件的导入
// import UserNutritionGoals from '@/views/users/UserNutritionGoals'
// import UserCalorieRecords from '@/views/users/UserCalorieRecords'
// import UserPreferences from '@/views/users/UserPreferences'

// 删除这些未实现的导入
// import RestaurantList from '@/views/restaurants/RestaurantList'
// import RestaurantDetail from '@/views/restaurants/RestaurantDetail'
// import RestaurantMenu from '@/views/restaurants/RestaurantMenu'
// import AlgorithmParams from '@/views/recommendation/AlgorithmParams'
// import RecommendationRules from '@/views/recommendation/RecommendationRules'
// import RecommendationResults from '@/views/recommendation/RecommendationResults'
// import NutritionGoalsStats from '@/views/statistics/NutritionGoalsStats'
// import UserPreferencesStats from '@/views/statistics/UserPreferencesStats'
// import PopularFoodsStats from '@/views/statistics/PopularFoodsStats'
// import NutritionParams from '@/views/settings/NutritionParams'
// import SystemNotifications from '@/views/settings/SystemNotifications'
// import UserFeedbacks from '@/views/settings/UserFeedbacks'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { public: true }
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: { public: true }
    },
    {
      path: '/',
      component: Layout,
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: Dashboard,
          meta: { title: '仪表盘' }
        },
        {
          path: 'users',
          name: 'UserList',
          component: UserList,
          meta: { title: '用户列表' }
        },
        {
          path: 'users/:id',
          name: 'UserDetail',
          component: UserDetail,
          meta: { title: '用户详情' }
        },
        {
          path: 'restaurants',
          name: 'RestaurantList',
          component: RestaurantList,
          meta: { title: '餐厅列表' }
        },
        {
          path: 'restaurants/:id',
          name: 'RestaurantDetail',
          component: RestaurantDetail,
          meta: { title: '餐厅详情' }
        }
      ]
    },
    {
      path: '*',
      redirect: '/dashboard'
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  const requiresAuth = !to.matched.some(record => record.meta.public)
  
  // 如果需要认证但用户未登录，重定向到登录页
  if (requiresAuth && !isLoggedIn()) {
    next('/login')
  } else {
    next()
  }
})

export default router 
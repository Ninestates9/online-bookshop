import component from 'element-plus/es/components/tree-select/src/tree-select-option.mjs'
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

// createRouter 创建路由实例，===> new VueRouter()
// history 是路由模式，hash模式，history模式
// createWebHistory() 是开启history模块 
// createWebHashHistory() 是开启hash模式   

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomePage/index.vue')
  },
  {
    path: '/SignIn',
    name: 'signin',
    component: () => import('../views/SignIn/index.vue')
  },
  {
    path: '/SignUp',
    name: 'signup',
    component: () => import('../views/SignUp/index.vue')
  },
  {
    path: '/Customer',
    name: 'customer',
    component: () => import('../views/Customer/index.vue'),
    redirect: '/BookBrowser',
    children: [
      {
        path: '/BookBrowser',
        name: 'BookBrowser',
        component: () => import('../views/Customer/BookBrowser/index.vue')
      },
      {
        path: '/CustomerInfo',
        name: 'CustomerInfo',
        component: () => import('../views/Customer/CustomerInfo/index.vue')
      },
      {
        path: '/History',
        name: 'History',
        component: () => import('../views/Customer/History/index.vue')
      }
    ]

  }
] as RouteRecordRaw[]
const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router

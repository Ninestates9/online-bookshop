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
    component: () => import('../views/HomePage/index.vue'),
    redirect: '/SignIn'
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
    redirect: '/Customer/BookBrowser',
    children: [
      {
        path: '/Customer/BookBrowser',
        name: 'BookBrowser',
        component: () => import('../views/Customer/BookBrowser/index.vue')
      },
      {
        path: '/Customer/CustomerInfo',
        name: 'CustomerInfo',
        component: () => import('../views/Customer/CustomerInfo/index.vue')
      },
      {
        path: '/Customer/History',
        name: 'History',
        component: () => import('../views/Customer/History/index.vue')
      },
      {
        path: '/Customer/Cart',
        name: 'Cart',
        component: () => import('../views/Customer/Cart/index.vue')
      },
      {
        path: '/Customer/Message',
        name: 'Message',
        component: () => import('../views/Customer/Message/index.vue')
      },
    ]

  },
  {
    path: '/Bookshop',
    name: 'Bookshop',
    component: () => import('../views/Bookshop/index.vue'),
    redirect: '/Bookshop/Storage',
    children: [
      {
        path: '/Bookshop/Storage',
        name: 'Storage',
        component: () => import('../views/Bookshop/Storage/index.vue')
      },
      {
        path: '/Bookshop/Order',
        name: 'Order',
        component: () => import('../views/Bookshop/Order/index.vue')
      },
      {
        path: '/Bookshop/Usermessage',
        name: 'Usermessage',
        component: () => import('../views/Bookshop/Usermessage/index.vue')
      },
      {
        path: '/Bookshop/UserInfo',
        name: 'UserInfo',
        component: () => import('../views/Bookshop/UserInfo/index.vue')
      },
      {
        path: '/Bookshop/MissingRecord',
        name: 'MissingRecord',
        component: () => import('../views/Bookshop/MissingRecord/index.vue')
      },
      {
        path: '/Bookshop/Purchase',
        name: 'Purchase',
        component: () => import('../views/Bookshop/Purchase/index.vue')
      },
      {
        path: '/Bookshop/Provider',
        name: 'Provider',
        component: () => import('../views/Bookshop/Provider/index.vue')
      },
      
    ]
  }
] as RouteRecordRaw[]
const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router

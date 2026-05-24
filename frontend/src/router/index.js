import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/conversations',
    name: 'ConversationList',
    component: () => import('@/views/ConversationList.vue'),
    meta: { title: '对话列表' }
  },
  {
    path: '/conversations/:id',
    name: 'ConversationDetail',
    component: () => import('@/views/ConversationDetail.vue'),
    meta: { title: '对话详情' }
  },
  {
    path: '/stats',
    name: 'Stats',
    component: () => import('@/views/StatsView.vue'),
    meta: { title: '统计分析' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/SettingsView.vue'),
    meta: { title: '设置' }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：更新页面标题
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'AI对话管理器'} - AI对话记录管理器`
  next()
})

export default router

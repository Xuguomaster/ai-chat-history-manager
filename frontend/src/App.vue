<template>
  <el-container class="app-container">
    <!-- 左侧导航菜单 -->
    <el-aside :width="isCollapse ? '64px' : '220px'" class="app-aside">
      <div class="logo-area">
        <el-icon :size="28"><ChatDotRound /></el-icon>
        <span v-show="!isCollapse" class="logo-text">AI对话管理器</span>
      </div>

      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        router
        background-color="transparent"
        text-color="var(--text-secondary)"
        active-text-color="var(--primary-color)"
        class="side-menu"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <template #title>首页</template>
        </el-menu-item>

        <el-menu-item index="/conversations">
          <el-icon><ChatLineSquare /></el-icon>
          <template #title>对话列表</template>
        </el-menu-item>

        <el-menu-item index="/stats">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>统计分析</template>
        </el-menu-item>

        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <template #title>设置</template>
        </el-menu-item>
      </el-menu>

      <!-- 折叠按钮 -->
      <div class="collapse-btn" @click="isCollapse = !isCollapse">
        <el-icon :size="18">
          <Fold v-if="!isCollapse" />
          <Expand v-else />
        </el-icon>
      </div>
    </el-aside>

    <!-- 右侧内容区 -->
    <el-container class="main-container">
      <!-- 顶部栏 -->
      <el-header class="app-header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="breadcrumbTitle">{{ breadcrumbTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <!-- 主题切换 -->
          <el-switch
            v-model="isDark"
            inline-prompt
            active-text="暗色"
            inactive-text="亮色"
            @change="toggleTheme"
          />
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeFilled,
  ChatLineSquare,
  ChatDotRound,
  DataAnalysis,
  Setting,
  Fold,
  Expand
} from '@element-plus/icons-vue'

const route = useRoute()

// 侧边栏折叠状态
const isCollapse = ref(false)

// 深色主题状态
const isDark = ref(false)

// 当前激活的菜单项
const activeMenu = computed(() => {
  // 对话详情页也高亮"对话列表"
  if (route.path.startsWith('/conversations')) return '/conversations'
  return route.path
})

// 面包屑标题
const breadcrumbTitle = computed(() => {
  const titles = {
    '/conversations': '对话列表',
    '/stats': '统计分析',
    '/settings': '设置'
  }
  // 对话详情页
  if (route.path.startsWith('/conversations/') && route.params.id) {
    return '对话详情'
  }
  return titles[route.path] || ''
})

// 切换深色/浅色主题
const toggleTheme = (dark) => {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
}
</script>

<style scoped>
.app-container {
  height: 100vh;
  overflow: hidden;
}

/* 左侧导航栏 */
.app-aside {
  background-color: var(--bg-aside);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  overflow: hidden;
}

/* Logo区域 */
.logo-area {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--primary-color);
  font-size: 16px;
  font-weight: 700;
  border-bottom: 1px solid var(--border-color);
  white-space: nowrap;
  overflow: hidden;
}

.logo-text {
  font-size: 15px;
}

/* 侧边菜单 */
.side-menu {
  flex: 1;
  border-right: none !important;
  padding: 8px 0;
}

.side-menu .el-menu-item {
  height: 48px;
  line-height: 48px;
  margin: 2px 8px;
  border-radius: 8px;
}

.side-menu .el-menu-item:hover {
  background-color: var(--bg-hover);
}

.side-menu .el-menu-item.is-active {
  background-color: var(--primary-color-light);
  color: var(--primary-color);
  font-weight: 600;
}

/* 折叠按钮 */
.collapse-btn {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--text-secondary);
  border-top: 1px solid var(--border-color);
  transition: color 0.2s;
}

.collapse-btn:hover {
  color: var(--primary-color);
}

/* 右侧主容器 */
.main-container {
  flex-direction: column;
  overflow: hidden;
}

/* 顶部栏 */
.app-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
  padding: 0 24px;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 主内容区 */
.app-main {
  flex: 1;
  overflow-y: auto;
  background-color: var(--bg-main);
  padding: 24px;
}
</style>

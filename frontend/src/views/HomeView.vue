<template>
  <div class="home-view">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <h1 class="welcome-title">AI 对话记录管理器</h1>
      <p class="welcome-desc">
        集中管理你的 AI 对话历史，支持搜索、分类、统计分析等功能。
        让你的每一次 AI 交互都有迹可循。
      </p>
      <el-button type="primary" size="large" @click="$router.push('/conversations')">
        <el-icon><ChatLineSquare /></el-icon>
        查看对话列表
      </el-button>
    </div>

    <!-- 快速统计卡片 -->
    <el-row :gutter="20" class="stats-cards">
      <el-col :xs="12" :sm="6" v-for="item in statCards" :key="item.label">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" :style="{ backgroundColor: item.color + '20', color: item.color }">
            <el-icon :size="28"><component :is="item.icon" /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ item.value }}</div>
            <div class="stat-label">{{ item.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 功能介绍 -->
    <el-row :gutter="20" class="features-section">
      <el-col :xs="24" :sm="8" v-for="feature in features" :key="feature.title">
        <el-card shadow="hover" class="feature-card">
          <el-icon :size="36" :color="feature.color" class="feature-icon">
            <component :is="feature.icon" />
          </el-icon>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ChatLineSquare, Document, Search, DataAnalysis } from '@element-plus/icons-vue'
import { getConversationStats } from '@/api'

// 统计卡片数据
const statCards = ref([
  { label: '总对话数', value: '--', icon: 'ChatLineSquare', color: '#409EFF' },
  { label: '总消息数', value: '--', icon: 'Document', color: '#67C23A' },
  { label: '本周新增', value: '--', icon: 'Search', color: '#E6A23C' },
  { label: '标签分类', value: '--', icon: 'DataAnalysis', color: '#F56C6C' }
])

// 功能介绍
const features = [
  {
    title: '对话管理',
    desc: '导入、浏览和管理你的所有 AI 对话记录，支持多种格式导入。',
    icon: 'ChatLineSquare',
    color: '#409EFF'
  },
  {
    title: '全文搜索',
    desc: '强大的全文搜索功能，快速定位任意对话中的关键内容。',
    icon: 'Search',
    color: '#67C23A'
  },
  {
    title: '统计分析',
    desc: '可视化图表展示对话趋势、使用频率等统计数据。',
    icon: 'DataAnalysis',
    color: '#E6A23C'
  }
]

// 加载统计数据
onMounted(async () => {
  try {
    const data = await getConversationStats()
    if (data) {
      statCards.value[0].value = data.total_conversations ?? 0
      statCards.value[1].value = data.total_messages ?? 0
      statCards.value[2].value = data.week_new ?? 0
      statCards.value[3].value = data.total_tags ?? 0
    }
  } catch {
    // 后端未就绪时使用默认值
    statCards.value.forEach((item) => { item.value = 0 })
  }
})
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
}

/* 欢迎区域 */
.welcome-section {
  text-align: center;
  padding: 48px 0 40px;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.welcome-desc {
  font-size: 16px;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 32px;
  line-height: 1.6;
}

/* 统计卡片 */
.stats-cards {
  margin-bottom: 40px;
}

.stat-card {
  border-radius: 12px;
  margin-bottom: 16px;
}

.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

/* 功能介绍 */
.features-section {
  margin-bottom: 40px;
}

.feature-card {
  border-radius: 12px;
  text-align: center;
  margin-bottom: 16px;
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-icon {
  margin-bottom: 16px;
}

.feature-card h3 {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.feature-card p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>

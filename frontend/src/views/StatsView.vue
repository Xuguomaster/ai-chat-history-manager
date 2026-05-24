<template>
  <div class="stats-view">
    <h2 class="page-title">统计分析</h2>

    <!-- 概览卡片 -->
    <el-row :gutter="20" class="overview-cards">
      <el-col :xs="12" :sm="6" v-for="item in overviewStats" :key="item.label">
        <el-card shadow="hover" class="overview-card">
          <div class="overview-value">{{ item.value }}</div>
          <div class="overview-label">{{ item.label }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20">
      <!-- 对话趋势图 -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <span class="chart-title">对话趋势</span>
          </template>
          <v-chart class="chart" :option="trendOption" autoresize />
        </el-card>
      </el-col>

      <!-- 消息类型分布 -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <span class="chart-title">消息角色分布</span>
          </template>
          <v-chart class="chart" :option="roleOption" autoresize />
        </el-card>
      </el-col>

      <!-- 标签使用统计 -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <span class="chart-title">标签使用统计</span>
          </template>
          <v-chart class="chart" :option="tagOption" autoresize />
        </el-card>
      </el-col>

      <!-- 每日活跃时段 -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <span class="chart-title">每日活跃时段</span>
          </template>
          <v-chart class="chart" :option="hourOption" autoresize />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { getStats } from '@/api'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

// 概览统计数据
const overviewStats = ref([
  { label: '总对话数', value: '--' },
  { label: '总消息数', value: '--' },
  { label: '平均消息数/对话', value: '--' },
  { label: '最活跃日期', value: '--' }
])

// 统计数据
const statsData = ref(null)

// 对话趋势图配置
const trendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: {
    type: 'category',
    data: statsData.value?.trend_dates || ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    axisLine: { lineStyle: { color: '#ccc' } },
    axisLabel: { color: '#999' }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#f0f0f0' } },
    axisLabel: { color: '#999' }
  },
  series: [{
    name: '对话数',
    type: 'line',
    smooth: true,
    data: statsData.value?.trend_counts || [5, 8, 12, 7, 15, 10, 6],
    areaStyle: { opacity: 0.15 },
    lineStyle: { width: 3 },
    itemStyle: { color: '#409EFF' }
  }]
}))

// 消息角色分布图配置
const roleOption = computed(() => ({
  tooltip: { trigger: 'item' },
  legend: { bottom: '0', left: 'center' },
  series: [{
    name: '消息角色',
    type: 'pie',
    radius: ['40%', '70%'],
    avoidLabelOverlap: false,
    itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
    label: { show: false },
    emphasis: { label: { show: true, fontSize: 16, fontWeight: 'bold' } },
    data: statsData.value?.role_distribution || [
      { value: 1048, name: '用户', itemStyle: { color: '#409EFF' } },
      { value: 735, name: '助手', itemStyle: { color: '#67C23A' } },
      { value: 80, name: '系统', itemStyle: { color: '#E6A23C' } }
    ]
  }]
}))

// 标签使用统计图配置
const tagOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: {
    type: 'category',
    data: statsData.value?.tag_names || ['编程', '写作', '翻译', '学习', '工作'],
    axisLine: { lineStyle: { color: '#ccc' } },
    axisLabel: { color: '#999' }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#f0f0f0' } },
    axisLabel: { color: '#999' }
  },
  series: [{
    name: '使用次数',
    type: 'bar',
    data: statsData.value?.tag_counts || [120, 80, 60, 45, 30],
    itemStyle: {
      borderRadius: [6, 6, 0, 0],
      color: {
        type: 'linear',
        x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: '#409EFF' },
          { offset: 1, color: '#79bbff' }
        ]
      }
    }
  }]
}))

// 每日活跃时段图配置
const hourOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: {
    type: 'category',
    data: Array.from({ length: 24 }, (_, i) => `${i}:00`),
    axisLine: { lineStyle: { color: '#ccc' } },
    axisLabel: { color: '#999', interval: 2 }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#f0f0f0' } },
    axisLabel: { color: '#999' }
  },
  series: [{
    name: '消息数',
    type: 'bar',
    data: statsData.value?.hourly_counts || [2, 1, 0, 0, 1, 3, 8, 15, 22, 18, 12, 10, 14, 16, 20, 18, 15, 12, 10, 8, 6, 4, 3, 2],
    itemStyle: {
      borderRadius: [4, 4, 0, 0],
      color: {
        type: 'linear',
        x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: '#67C23A' },
          { offset: 1, color: '#95d475' }
        ]
      }
    }
  }]
}))

// 加载统计数据
onMounted(async () => {
  try {
    const data = await getStats()
    statsData.value = data
    if (data) {
      overviewStats.value[0].value = data.total_conversations ?? 0
      overviewStats.value[1].value = data.total_messages ?? 0
      overviewStats.value[2].value = data.avg_messages ?? 0
      overviewStats.value[3].value = data.most_active_date ?? '--'
    }
  } catch {
    // 后端未就绪时使用默认占位数据
  }
})
</script>

<style scoped>
.stats-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 24px;
}

/* 概览卡片 */
.overview-cards {
  margin-bottom: 24px;
}

.overview-card {
  border-radius: 12px;
  text-align: center;
  margin-bottom: 16px;
}

.overview-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary-color);
}

.overview-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

/* 图表卡片 */
.chart-card {
  border-radius: 12px;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.chart {
  height: 320px;
  width: 100%;
}
</style>

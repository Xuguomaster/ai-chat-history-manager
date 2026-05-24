<template>
  <div class="conversation-list">
    <!-- 搜索和筛选栏 -->
    <div class="filter-bar">
      <SearchBar @search="handleSearch" />
      <div class="filter-actions">
        <el-select
          v-model="filterTag"
          placeholder="按标签筛选"
          clearable
          style="width: 160px"
        >
          <el-option
            v-for="tag in tags"
            :key="tag"
            :label="tag"
            :value="tag"
          />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          style="width: 260px"
          value-format="YYYY-MM-DD"
          @change="loadConversations"
        />
      </div>
    </div>

    <!-- 对话列表 -->
    <div v-loading="loading" class="conversation-cards">
      <el-empty v-if="!loading && conversations.length === 0" description="暂无对话记录" />

      <el-card
        v-for="conv in conversations"
        :key="conv.id"
        shadow="hover"
        class="conversation-card"
        @click="$router.push(`/conversations/${conv.id}`)"
      >
        <div class="card-header">
          <h3 class="card-title">{{ conv.title || '未命名对话' }}</h3>
          <el-tag v-if="conv.tag" size="small" type="info">{{ conv.tag }}</el-tag>
        </div>
        <p class="card-preview">{{ conv.preview || '暂无预览内容...' }}</p>
        <div class="card-meta">
          <span class="meta-item">
            <el-icon><ChatDotRound /></el-icon>
            {{ conv.message_count || 0 }} 条消息
          </span>
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            {{ formatDate(conv.created_at) }}
          </span>
        </div>
      </el-card>
    </div>

    <!-- 分页 -->
    <div class="pagination-wrapper" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadConversations"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ChatDotRound, Calendar } from '@element-plus/icons-vue'
import { getConversations } from '@/api'
import SearchBar from '@/components/SearchBar.vue'

// 对话列表数据
const conversations = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 搜索和筛选条件
const searchKeyword = ref('')
const filterTag = ref('')
const dateRange = ref(null)

// 标签列表（示例数据，实际应从后端获取）
const tags = ref(['编程', '写作', '翻译', '学习', '工作', '其他'])

// 加载对话列表
async function loadConversations() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (searchKeyword.value) params.search = searchKeyword.value
    if (filterTag.value) params.tag = filterTag.value
    if (dateRange.value && dateRange.value.length === 2) {
      params.date_from = dateRange.value[0]
      params.date_to = dateRange.value[1]
    }

    const data = await getConversations(params)
    conversations.value = data.items || data.results || []
    total.value = data.total || 0
  } catch {
    conversations.value = []
  } finally {
    loading.value = false
  }
}

// 处理搜索
function handleSearch(keyword) {
  searchKeyword.value = keyword
  currentPage.value = 1
  loadConversations()
}

// 格式化日期
function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadConversations()
})
</script>

<style scoped>
.conversation-list {
  max-width: 1000px;
  margin: 0 auto;
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.filter-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* 对话卡片列表 */
.conversation-cards {
  min-height: 200px;
}

.conversation-card {
  margin-bottom: 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.conversation-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  margin-right: 12px;
}

.card-preview {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>

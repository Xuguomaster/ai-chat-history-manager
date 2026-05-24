﻿<template>
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
          <el-option v-for="tag in tags" :key="tag" :label="tag" :value="tag" />
        </el-select>
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新建对话
        </el-button>
      </div>
    </div>

    <!-- 对话列表 -->
    <div v-loading="loading" class="conversation-cards">
      <el-empty v-if="!loading && conversations.length === 0" description="暂无对话记录" />
      <el-card v-for="conv in conversations" :key="conv.id" shadow="hover" class="conversation-card" @click="$router.push(`/conversations/${conv.id}`)">
        <div class="card-header">
          <h3 class="card-title">{{ conv.title || '未命名对话' }}</h3>
          <el-tag v-if="conv.tags" size="small" type="info">{{ conv.tags }}</el-tag>
        </div>
        <p class="card-preview">{{ conv.preview || conv.source || '点击查看详情...' }}</p>
        <div class="card-meta">
          <span class="meta-item"><el-icon><ChatDotRound /></el-icon> {{ conv.message_count || 0 }} 条消息</span>
          <span class="meta-item"><el-icon><Calendar /></el-icon> {{ formatDate(conv.created_at) }}</span>
          <span class="meta-item" v-if="conv.source"><el-tag size="small" effect="plain">{{ conv.source }}</el-tag></span>
        </div>
      </el-card>
    </div>

    <!-- 分页 -->
    <div class="pagination-wrapper" v-if="total > pageSize">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="total" layout="prev, pager, next" @current-change="loadConversations" />
    </div>

    <!-- 新建对话弹窗 -->
    <el-dialog v-model="showCreateDialog" title="新建对话" width="500px">
      <el-form :model="createForm" label-width="80px">
        <el-form-item label="对话标题">
          <el-input v-model="createForm.title" placeholder="输入对话标题..." />
        </el-form-item>
        <el-form-item label="来源">
          <el-select v-model="createForm.source" placeholder="选择AI来源" style="width: 100%">
            <el-option label="ChatGPT" value="ChatGPT" />
            <el-option label="Claude" value="Claude" />
            <el-option label="文心一言" value="文心一言" />
            <el-option label="Mimo" value="Mimo" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="createForm.tags" placeholder="用逗号分隔，如：学习,编程" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" :loading="creating" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChatDotRound, Calendar, Plus } from '@element-plus/icons-vue'
import { getConversations, createConversation } from '@/api'
import { ElMessage } from 'element-plus'
import SearchBar from '@/components/SearchBar.vue'

const router = useRouter()

const conversations = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const searchKeyword = ref('')
const filterTag = ref('')
const tags = ref(['编程', '写作', '翻译', '学习', '工作', '其他'])

// 新建对话
const showCreateDialog = ref(false)
const creating = ref(false)
const createForm = ref({ title: '', source: 'ChatGPT', tags: '' })

async function loadConversations() {
  loading.value = true
  try {
    const params = { skip: (currentPage.value - 1) * pageSize.value, limit: pageSize.value }
    if (searchKeyword.value) params.keyword = searchKeyword.value
    if (filterTag.value) params.tag = filterTag.value
    const data = await getConversations(params)
    conversations.value = Array.isArray(data) ? data : (data.items || data.results || [])
    total.value = Array.isArray(data) ? data.length : (data.total || 0)
  } catch {
    conversations.value = []
  } finally {
    loading.value = false
  }
}

async function handleCreate() {
  if (!createForm.value.title.trim()) {
    ElMessage.warning('请输入对话标题')
    return
  }
  creating.value = true
  try {
    const conv = await createConversation({
      title: createForm.value.title,
      source: createForm.value.source,
      tags: createForm.value.tags
    })
    showCreateDialog.value = false
    createForm.value = { title: '', source: 'ChatGPT', tags: '' }
    ElMessage.success('创建成功！')
    await loadConversations()
    if (conv && conv.id) {
      router.push(`/conversations/${conv.id}`)
    }
  } catch {
    ElMessage.error('创建失败')
  } finally {
    creating.value = false
  }
}

function handleSearch(keyword) {
  searchKeyword.value = keyword
  currentPage.value = 1
  loadConversations()
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'
  })
}

onMounted(() => loadConversations())
</script>

<style scoped>
.conversation-list { max-width: 1000px; margin: 0 auto; }
.filter-bar { display: flex; flex-wrap: wrap; align-items: center; gap: 16px; margin-bottom: 24px; }
.filter-actions { display: flex; gap: 12px; flex-wrap: wrap; }
.conversation-cards { min-height: 200px; }
.conversation-card { margin-bottom: 16px; border-radius: 12px; cursor: pointer; transition: transform 0.2s; }
.conversation-card:hover { transform: translateY(-2px); }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.card-title { font-size: 16px; font-weight: 600; color: var(--text-primary); margin: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; margin-right: 12px; }
.card-preview { font-size: 14px; color: var(--text-secondary); line-height: 1.5; margin: 0 0 12px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.card-meta { display: flex; gap: 20px; font-size: 12px; color: var(--text-tertiary); }
.meta-item { display: flex; align-items: center; gap: 4px; }
.pagination-wrapper { display: flex; justify-content: center; margin-top: 24px; }
</style>
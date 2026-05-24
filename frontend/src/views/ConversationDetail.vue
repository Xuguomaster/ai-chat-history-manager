<template>
  <div class="conversation-detail">
    <!-- 返回按钮和对话标题 -->
    <div class="detail-header">
      <el-button text @click="$router.push('/conversations')">
        <el-icon><ArrowLeft /></el-icon>
        返回列表
      </el-button>
      <div class="detail-title-area" v-if="conversation">
        <h2 class="detail-title">{{ conversation.title || '未命名对话' }}</h2>
        <el-tag v-if="conversation.tag" size="small" type="info">{{ conversation.tag }}</el-tag>
      </div>
    </div>

    <!-- 消息列表 -->
    <div v-loading="loading" class="messages-container">
      <el-empty v-if="!loading && messages.length === 0" description="暂无消息" />

      <div v-for="msg in messages" :key="msg.id" class="message-wrapper">
        <MessageBubble :message="msg" />
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination-wrapper" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadMessages"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getConversation, getMessages } from '@/api'
import MessageBubble from '@/components/MessageBubble.vue'

const route = useRoute()

// 对话详情
const conversation = ref(null)

// 消息列表
const messages = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(50)
const total = ref(0)

// 加载对话详情
async function loadConversation() {
  try {
    conversation.value = await getConversation(route.params.id)
  } catch {
    conversation.value = null
  }
}

// 加载消息列表
async function loadMessages() {
  loading.value = true
  try {
    const data = await getMessages(route.params.id, {
      page: currentPage.value,
      page_size: pageSize.value
    })
    messages.value = data.items || data.results || []
    total.value = data.total || 0
  } catch {
    messages.value = []
  } finally {
    loading.value = false
  }
}

// 监听路由参数变化（切换对话时重新加载）
watch(() => route.params.id, () => {
  if (route.params.id) {
    currentPage.value = 1
    loadConversation()
    loadMessages()
  }
})

onMounted(() => {
  loadConversation()
  loadMessages()
})
</script>

<style scoped>
.conversation-detail {
  max-width: 900px;
  margin: 0 auto;
}

/* 顶部信息栏 */
.detail-header {
  margin-bottom: 24px;
}

.detail-title-area {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.detail-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

/* 消息容器 */
.messages-container {
  min-height: 300px;
  padding: 16px 0;
}

.message-wrapper {
  margin-bottom: 16px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>

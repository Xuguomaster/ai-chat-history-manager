<template>
  <div class="conversation-detail">
    <div class="detail-header">
      <el-button text @click="$router.push('/conversations')">
        <el-icon><ArrowLeft /></el-icon>
        返回列表
      </el-button>
      <div class="detail-title-area" v-if="conversation">
        <h2 class="detail-title">{{ conversation.title || '未命名对话' }}</h2>
        <el-tag v-if="conversation.tags" size="small" type="info">{{ conversation.tags }}</el-tag>
      </div>
    </div>

    <div v-loading="loading" class="messages-container" ref="msgContainer">
      <el-empty v-if="!loading && messages.length === 0" description="暂无消息，在下方输入框发送第一条消息吧！" />
      <div v-for="msg in messages" :key="msg.id" class="message-wrapper">
        <MessageBubble :message="msg" />
      </div>
      <!-- AI思考中 -->
      <div v-if="aiThinking" class="message-wrapper">
        <div class="thinking-bubble">AI 思考中...</div>
      </div>
    </div>

    <div class="input-area">
      <el-input v-model="inputText" type="textarea" :rows="3" placeholder="输入消息内容..." :disabled="sending" @keydown.enter.ctrl="sendMessage" />
      <div class="input-actions">
        <el-select v-model="aiProvider" size="small" style="width: 120px" v-if="!sending">
          <el-option label="小米Mimo" value="mimo" />
          <el-option label="OpenAI" value="openai" />
          <el-option label="模拟回复" value="mock" />
        </el-select>
        <span class="input-hint" v-if="inputText">Ctrl + Enter 发送</span>
        <el-button type="primary" :loading="sending" :disabled="!inputText.trim()" @click="sendMessage">
          <el-icon><Promotion /></el-icon>
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, Promotion } from '@element-plus/icons-vue'
import { getConversation, getMessages, addMessage, aiChat } from '@/api'
import { ElMessage } from 'element-plus'
import MessageBubble from '@/components/MessageBubble.vue'

const route = useRoute()
const msgContainer = ref(null)
const conversation = ref(null)
const messages = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(50)
const total = ref(0)
const inputText = ref('')
const sending = ref(false)
const aiThinking = ref(false)
const aiProvider = ref('mock')

async function loadConversation() {
  try { conversation.value = await getConversation(route.params.id) } catch { conversation.value = null }
}

async function loadMessages() {
  loading.value = true
  try {
    const data = await getMessages(route.params.id, {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    messages.value = Array.isArray(data) ? data : (data.items || data.results || [])
    total.value = Array.isArray(data) ? data.length : (data.total || 0)
  } catch { messages.value = [] }
  finally { loading.value = false }
}

async function sendMessage() {
  const content = inputText.value.trim()
  if (!content || sending.value) return
  sending.value = true
  try {
    // 1. 保存用户消息
    const userMsg = await addMessage(route.params.id, { role: 'user', content })
    messages.value.push(userMsg)
    inputText.value = ''
    scrollToBottom()

    if (aiProvider.value === 'mock') {
      // 模拟回复
      setTimeout(async () => {
        const aiMsg = await addMessage(route.params.id, {
          role: 'assistant',
          content: '这是一条模拟的AI回复。接入Mimo API后可替换为真实AI回复。'
        })
        messages.value.push(aiMsg)
        scrollToBottom()
      }, 800)
    } else {
      // 真实AI调用
      aiThinking.value = true
      scrollToBottom()
      try {
        // 构建对话上下文
        const context = messages.value.slice(-20).map(m => ({
          role: m.role,
          content: m.content
        }))
        const result = await aiChat(context, aiProvider.value)
        const aiReply = result.reply || 'AI未返回有效回复'
        const aiMsg = await addMessage(route.params.id, { role: 'assistant', content: aiReply })
        messages.value.push(aiMsg)
      } catch (err) {
        ElMessage.error('AI服务暂不可用: ' + (err.response?.data?.detail || err.message))
        // 回退到模拟回复
        const fallback = await addMessage(route.params.id, {
          role: 'assistant',
          content: '(AI服务未配置，这是模拟回复。请在环境变量中设置 MIMO_API_KEY)'
        })
        messages.value.push(fallback)
      }
      aiThinking.value = false
      scrollToBottom()
    }
  } catch { ElMessage.error('发送失败，请重试') }
  finally { sending.value = false }
}

function scrollToBottom() {
  nextTick(() => { if (msgContainer.value) msgContainer.value.scrollTop = msgContainer.value.scrollHeight })
}

watch(() => route.params.id, () => {
  if (route.params.id) { currentPage.value = 1; inputText.value = ''; loadConversation(); loadMessages() }
})

onMounted(() => { loadConversation(); loadMessages() })
</script>

<style scoped>
.conversation-detail { max-width: 900px; margin: 0 auto; height: calc(100vh - 140px); display: flex; flex-direction: column; }
.detail-header { flex-shrink: 0; margin-bottom: 16px; }
.detail-title-area { display: flex; align-items: center; gap: 12px; margin-top: 8px; }
.detail-title { font-size: 22px; font-weight: 700; color: var(--text-primary); margin: 0; }
.messages-container { flex: 1; overflow-y: auto; padding: 16px 0; min-height: 0; }
.message-wrapper { margin-bottom: 16px; }
.thinking-bubble { display: inline-block; background: var(--bg-hover); color: var(--text-secondary); padding: 10px 16px; border-radius: 12px; font-size: 14px; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.5; } }
.input-area { flex-shrink: 0; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border-color); background: var(--bg-card); }
.input-actions { display: flex; justify-content: flex-end; align-items: center; gap: 12px; margin-top: 8px; }
.input-hint { font-size: 12px; color: var(--text-tertiary); }
</style>
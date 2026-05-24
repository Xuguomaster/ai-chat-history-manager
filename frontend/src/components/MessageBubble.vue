<template>
  <div class="message-bubble" :class="[`message-${message.role}`]">
    <!-- 头像 -->
    <div class="avatar">
      <el-avatar :size="36" :style="{ backgroundColor: avatarColor }">
        <el-icon :size="18">
          <User v-if="message.role === 'user'" />
          <Monitor v-else-if="message.role === 'assistant'" />
          <InfoFilled v-else />
        </el-icon>
      </el-avatar>
    </div>

    <!-- 消息内容 -->
    <div class="bubble-content">
      <div class="bubble-header">
        <span class="role-name">{{ roleLabel }}</span>
        <span class="message-time">{{ formatTime(message.created_at) }}</span>
      </div>
      <div class="bubble-body" v-html="formattedContent"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { User, Monitor, InfoFilled } from '@element-plus/icons-vue'

const props = defineProps({
  // 消息对象，包含 role, content, created_at 等字段
  message: {
    type: Object,
    required: true
  }
})

// 角色标签
const roleLabel = computed(() => {
  const labels = {
    user: '用户',
    assistant: 'AI 助手',
    system: '系统'
  }
  return labels[props.message.role] || props.message.role
})

// 头像颜色
const avatarColor = computed(() => {
  const colors = {
    user: '#409EFF',
    assistant: '#67C23A',
    system: '#E6A23C'
  }
  return colors[props.message.role] || '#909399'
})

// 格式化消息内容（简单的换行处理）
const formattedContent = computed(() => {
  if (!props.message.content) return ''
  return props.message.content
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
})

// 格式化时间
function formatTime(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.message-bubble {
  display: flex;
  gap: 12px;
  padding: 8px 0;
}

/* 用户消息：右对齐 */
.message-user {
  flex-direction: row-reverse;
}

/* 头像 */
.avatar {
  flex-shrink: 0;
}

/* 消息内容区域 */
.bubble-content {
  max-width: 75%;
}

.bubble-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.message-user .bubble-header {
  flex-direction: row-reverse;
}

.role-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.message-time {
  font-size: 11px;
  color: var(--text-tertiary);
}

/* 气泡主体 */
.bubble-body {
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.7;
  word-break: break-word;
}

/* 用户消息气泡 */
.message-user .bubble-body {
  background-color: var(--primary-color);
  color: #ffffff;
  border-top-right-radius: 4px;
}

/* 助手消息气泡 */
.message-assistant .bubble-body {
  background-color: var(--bg-bubble-assistant);
  color: var(--text-primary);
  border-top-left-radius: 4px;
}

/* 系统消息气泡 */
.message-system .bubble-body {
  background-color: var(--bg-bubble-system);
  color: var(--text-secondary);
  border-top-left-radius: 4px;
  font-style: italic;
  font-size: 13px;
}

/* 代码片段样式 */
.bubble-body :deep(code) {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
}

.message-user .bubble-body :deep(code) {
  background-color: rgba(255, 255, 255, 0.2);
}
</style>

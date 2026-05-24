import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' }
})

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    ElMessage.error(error.response?.data?.detail || '请求失败')
    return Promise.reject(error)
  }
)

// ==================== 对话 API ====================
export function getConversations(params = {}) {
  return request.get('/conversations', { params })
}
export function getConversation(id) {
  return request.get(`/conversations/${id}`)
}
export function deleteConversation(id) {
  return request.delete(`/conversations/${id}`)
}
export function getConversationStats() {
  return request.get('/stats')
}

// ==================== 消息 API ====================
export function getMessages(conversationId, params = {}) {
  return request.get(`/messages/conversation/${conversationId}`, { params })
}
export function addMessage(conversationId, data) {
  return request.post(`/messages/conversation/${conversationId}`, data)
}

// ==================== 统计 API ====================
export function getStats() {
  return request.get('/stats')
}

// ==================== AI API ====================
export function aiChat(messages, provider = 'mimo') {
  return request.post('/ai/chat', {
    messages,
    provider,
    temperature: 0.7,
    max_tokens: 2000
  })
}

// ==================== 创建 ====================
export function createConversation(data) {
  return request.post('/conversations', data)
}

export default request
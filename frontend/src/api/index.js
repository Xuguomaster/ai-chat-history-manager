import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 Axios 实例
const request = axios.create({
  baseURL: '/api/v1',
  timeout: 30000, // 请求超时时间：30秒
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 可在此处添加 token 等认证信息
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 统一错误处理
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// ==================== 对话相关 API ====================

/**
 * 获取对话列表
 * @param {Object} params - 查询参数 { page, page_size, search, tag, date_from, date_to }
 */
export function getConversations(params = {}) {
  return request.get('/conversations', { params })
}

/**
 * 获取单个对话详情
 * @param {string|number} id - 对话ID
 */
export function getConversation(id) {
  return request.get(`/conversations/${id}`)
}

/**
 * 删除对话
 * @param {string|number} id - 对话ID
 */
export function deleteConversation(id) {
  return request.delete(`/conversations/${id}`)
}

/**
 * 获取对话统计信息
 */
export function getConversationStats() {
  return request.get('/conversations/stats')
}

// ==================== 消息相关 API ====================

/**
 * 获取对话中的消息列表
 * @param {string|number} conversationId - 对话ID
 * @param {Object} params - 查询参数 { page, page_size }
 */
export function getMessages(conversationId, params = {}) {
  return request.get(`/conversations/${conversationId}/messages`, { params })
}

/**
 * 搜索消息
 * @param {Object} params - 查询参数 { keyword, page, page_size }
 */
export function searchMessages(params = {}) {
  return request.get('/messages/search', { params })
}

// ==================== 统计相关 API ====================

/**
 * 获取全局统计数据
 */
export function getStats() {
  return request.get('/stats')
}

/**
 * 获取趋势数据
 * @param {Object} params - 查询参数 { period }
 */
export function getTrendStats(params = {}) {
  return request.get('/stats/trend', { params })
}

export default request

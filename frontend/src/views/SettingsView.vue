<template>
  <div class="settings-view">
    <h2 class="page-title">设置</h2>

    <el-row :gutter="20">
      <!-- 通用设置 -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="settings-card">
          <template #header>
            <span class="card-title">通用设置</span>
          </template>

          <el-form label-width="120px" label-position="left">
            <el-form-item label="主题模式">
              <el-switch
                v-model="isDark"
                active-text="深色模式"
                inactive-text="浅色模式"
                @change="toggleTheme"
              />
            </el-form-item>

            <el-form-item label="每页显示条数">
              <el-select v-model="pageSize" style="width: 200px">
                <el-option :value="10" label="10 条" />
                <el-option :value="20" label="20 条" />
                <el-option :value="50" label="50 条" />
                <el-option :value="100" label="100 条" />
              </el-select>
            </el-form-item>

            <el-form-item label="语言">
              <el-select v-model="language" style="width: 200px">
                <el-option value="zh-CN" label="简体中文" />
                <el-option value="en-US" label="English" />
              </el-select>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 数据管理 -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="settings-card">
          <template #header>
            <span class="card-title">数据管理</span>
          </template>

          <el-form label-width="120px" label-position="left">
            <el-form-item label="导入数据">
              <el-button type="primary" plain>
                <el-icon><Upload /></el-icon>
                选择文件导入
              </el-button>
              <p class="form-tip">支持 JSON、CSV 格式的对话记录文件</p>
            </el-form-item>

            <el-form-item label="导出数据">
              <el-button type="success" plain>
                <el-icon><Download /></el-icon>
                导出全部数据
              </el-button>
              <p class="form-tip">将所有对话记录导出为 JSON 文件</p>
            </el-form-item>

            <el-form-item label="清除缓存">
              <el-button type="danger" plain @click="handleClearCache">
                <el-icon><Delete /></el-icon>
                清除本地缓存
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 关于 -->
      <el-col :span="24">
        <el-card shadow="hover" class="settings-card">
          <template #header>
            <span class="card-title">关于</span>
          </template>
          <div class="about-info">
            <p><strong>AI对话记录管理器</strong> v1.0.0</p>
            <p class="about-desc">
              一款用于管理和分析 AI 对话历史记录的工具应用。
              支持多种格式的对话记录导入、全文搜索、数据可视化统计等功能。
            </p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Upload, Download, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 设置项
const isDark = ref(document.documentElement.getAttribute('data-theme') === 'dark')
const pageSize = ref(20)
const language = ref('zh-CN')

// 切换主题
function toggleTheme(dark) {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
}

// 清除缓存
function handleClearCache() {
  ElMessageBox.confirm('确定要清除本地缓存吗？此操作不可恢复。', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    localStorage.clear()
    ElMessage.success('缓存已清除')
  }).catch(() => {})
}
</script>

<style scoped>
.settings-view {
  max-width: 1000px;
  margin: 0 auto;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.settings-card {
  border-radius: 12px;
  margin-bottom: 20px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.form-tip {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 4px;
}

.about-info p {
  color: var(--text-secondary);
  line-height: 1.8;
}

.about-desc {
  margin-top: 8px;
  font-size: 14px;
}
</style>

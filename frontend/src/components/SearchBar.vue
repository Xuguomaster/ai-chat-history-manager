<template>
  <div class="search-bar">
    <el-input
      v-model="keyword"
      placeholder="搜索对话内容..."
      clearable
      :prefix-icon="Search"
      size="large"
      class="search-input"
      @keyup.enter="handleSearch"
      @clear="handleClear"
    >
      <template #append>
        <el-button :icon="Search" @click="handleSearch">搜索</el-button>
      </template>
    </el-input>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

const emit = defineEmits(['search'])

// 搜索关键词
const keyword = ref('')

// 触发搜索
function handleSearch() {
  emit('search', keyword.value.trim())
}

// 清空搜索
function handleClear() {
  keyword.value = ''
  emit('search', '')
}
</script>

<style scoped>
.search-bar {
  flex: 1;
  min-width: 240px;
}

.search-input {
  max-width: 400px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 8px 0 0 8px;
}

.search-input :deep(.el-input-group__append) {
  border-radius: 0 8px 8px 0;
  background-color: var(--primary-color);
  color: #fff;
  border-color: var(--primary-color);
}

.search-input :deep(.el-input-group__append:hover) {
  background-color: var(--primary-color-hover);
}
</style>

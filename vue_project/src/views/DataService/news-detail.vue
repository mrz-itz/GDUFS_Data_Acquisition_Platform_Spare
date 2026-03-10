<template>
  <div class="news-detail">
    <div v-if="loading" class="loading-state">加载中...</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>
    <template v-else-if="news">
      <div class="detail-header">
        <button class="back-btn" @click="goBack">返回</button>
      </div>
      <article class="detail-card">
        <h1 class="detail-title">{{ news.title || '无标题' }}</h1>
        <div class="detail-meta">
          <span v-if="news.source" class="meta-item source">来源：{{ news.source }}</span>
          <span v-if="news.pub_time" class="meta-item time">{{ formatTime(news.pub_time) }}</span>
          <span v-if="news.location" class="meta-item location">语言/地区：{{ news.location }}</span>
        </div>
        <div class="book-page abstract-page">
          <h3 class="book-page-title">摘要</h3>
          <p class="detail-abstract">{{ news.abstract || '暂无摘要' }}</p>
        </div>
        <div class="book-page body-page">
          <h3 class="book-page-title">正文</h3>
          <div class="detail-body" v-html="bodyHtml"></div>
          <p v-if="!news.body" class="no-content">暂无正文</p>
        </div>
        <div class="detail-footer">
          <a
            v-if="news.request_url"
            :href="news.request_url"
            target="_blank"
            rel="noopener noreferrer"
            class="view-original"
          >
            查看原文
          </a>
        </div>
      </article>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { API_PREFIX } from '@/config/api'

const route = useRoute()
const router = useRouter()
const news = ref(null)
const loading = ref(true)
const error = ref('')

function goBack() {
  router.push('/data-service/data-search')
}

function formatTime(val) {
  if (!val) return '—'
  if (typeof val === 'string') return val
  if (val instanceof Date) return val.toLocaleString('zh-CN')
  return String(val)
}

const bodyHtml = computed(() => {
  if (!news.value || !news.value.body) return ''
  const text = String(news.value.body || '').replace(/\r\n/g, '\n')
  const escaped = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
  const paragraphs = escaped
    .split(/\n+/)
    .map((p) => p.trim())
    .filter(Boolean)
  if (!paragraphs.length) return ''
  return paragraphs.map((p) => `<p class="body-para">${p}</p>`).join('')
})

async function fetchNews() {
  const id = route.params.id
  if (!id) {
    error.value = '缺少新闻 ID'
    loading.value = false
    return
  }
  loading.value = true
  error.value = ''
  news.value = null
  try {
    const res = await fetch(`${API_PREFIX}/dashboard/news/${id}`)
    if (res.status === 404) {
      error.value = '新闻不存在'
      return
    }
    if (!res.ok) {
      error.value = '加载失败，请稍后重试'
      return
    }
    const data = await res.json()
    news.value = {
      id: data.id,
      title: data.title ?? '',
      abstract: data.abstract ?? '',
      body: data.body ?? '',
      pub_time: data.pub_time,
      request_url: data.request_url,
      source: data.source,
      location: data.location,
    }
  } catch (e) {
    error.value = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}

onMounted(fetchNews)
watch(() => route.params.id, fetchNews)
</script>

<style scoped>
.news-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 20px;
  background: #fff;
  min-height: 100%;
}
.loading-state,
.error-state {
  text-align: center;
  padding: 48px 20px;
  color: #666;
}
.error-state {
  color: #c00;
}
.detail-header {
  margin-bottom: 20px;
}
.back-btn {
  padding: 8px 16px;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
}
.back-btn:hover {
  background: #eee;
}
.detail-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  padding: 32px;
}
.detail-title {
  font-size: 1.5rem;
  line-height: 1.4;
  color: #1a1a1a;
  margin: 0 0 16px 0;
}
.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
  font-size: 0.875rem;
  color: #666;
}
.meta-item:not(:last-child)::after {
  content: '';
  margin-left: 16px;
}
.book-page {
  background: #faf9f6;
  border: 1px solid #e8e4dc;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.8);
}
.book-page-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #78716c;
  margin: 0 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #e8e4dc;
  letter-spacing: 0.05em;
}
.detail-abstract {
  color: #444;
  line-height: 1.75;
  margin: 0;
  font-size: 0.95rem;
}
.detail-body {
  line-height: 1.85;
  color: #333;
  word-break: break-word;
  font-size: 0.95rem;
  margin: 0;
}
.detail-body :deep(.body-para) {
  margin: 0 0 0.75em 0;
  text-indent: 2em;
  line-height: 1.85;
}
.detail-body :deep(br) {
  display: block;
}
.no-content {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0;
}
.detail-footer {
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}
.view-original {
  color: #409eff;
  text-decoration: none;
  font-size: 0.9rem;
}
.view-original:hover {
  text-decoration: underline;
}
</style>

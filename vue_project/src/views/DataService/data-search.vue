<template>
  <div class="search-page">
    <!-- 左侧固定边栏 -->
    <div class="left-sidebar">
      <div class="search-input-group">
        <div class="search-icon">Q</div>
        <input
          type="text"
          placeholder="请输入主题"
          class="search-input"
          v-model="searchParams.topic"
          @keyup.enter="performSearch"
        />
      </div>
      <div class="language-model">
        <span class="model-icon">◎</span>
        <span>语言模型</span>
      </div>
      <button class="add-theme-btn">+ 新增主题</button>
    </div>

    <!-- 右侧可滚动主内容区 -->
    <div class="main-content">
      <!-- 搜索条件区 -->
      <div class="search-condition">
        <h3>全部</h3>
        <div class="condition-group">
          <div class="condition-item">
            <span class="tag must-include">● 必须包含</span>
            <input
              type="text"
              placeholder="按Enter键对输入框进行赋值"
              v-model="searchParams.mustInclude"
              @keyup.enter="performSearch"
            />
          </div>
          <div class="condition-item">
            <span class="tag any-include"> 任意包含</span>
            <input
              type="text"
              placeholder="按Enter键对输入框进行赋值"
              v-model="searchParams.anyInclude"
              @keyup.enter="performSearch"
            />
          </div>
          <div class="condition-item">
            <span class="tag need-exclude">● 需要排除</span>
            <input
              type="text"
              placeholder="按Enter键对输入框进行赋值"
              v-model="searchParams.needExclude"
              @keyup.enter="performSearch"
            />
          </div>
        </div>
        <div class="action-btns">
          <button class="reset-btn" @click="resetSearch">重置</button>
          <button class="search-btn" @click="performSearch" :disabled="isLoading">
            {{ isLoading ? '搜索中...' : '搜索' }}
          </button>
        </div>
      </div>

      <!-- 筛选条件区 -->
      <div class="filter-section">
        <div class="filter-item">
          <span>发布时间</span>
          <button
            v-for="timeRange in timeRanges"
            :key="timeRange.value"
            :class="{ active: searchParams.publishTime === timeRange.value }"
            @click="setPublishTime(timeRange.value)"
          >
            {{ timeRange.label }}
          </button>
          <input
            type="datetime-local"
            v-model="searchParams.startTime"
            @change="onTimeRangeChange"
          />
          <span>至</span>
          <input type="datetime-local" v-model="searchParams.endTime" @change="onTimeRangeChange" />
        </div>
        <div class="filter-item">
          <span>命中位置</span>
          <button
            v-for="location in hitLocations"
            :key="location.value"
            :class="{ active: searchParams.hitLocation === location.value }"
            @click="handleHitLocationChange(location.value)"
          >
            {{ location.label }}
          </button>
        </div>
        <div class="filter-item">
          <span>数据源</span>
          <select v-model="searchParams.dataSource" @change="performSearch">
            <option value="">全部</option>
            <option v-for="source in dataSources" :key="source" :value="source">
              {{ source }}
            </option>
          </select>
          <span>语言</span>
          <select v-model="searchParams.language" @change="performSearch">
            <option value="">请选择</option>
            <option v-for="lang in languages" :key="lang" :value="lang">
              {{ lang }}
            </option>
          </select>
          <span>站点</span>
          <select v-model="searchParams.site" @change="performSearch">
            <option value="">请选择</option>
            <option v-for="site in sites" :key="site" :value="site">
              {{ site }}
            </option>
          </select>
        </div>
        <div class="filter-item">
          <input
            type="checkbox"
            id="select-all"
            v-model="selectAll"
            @change="handleSelectAllChange"
          />
          <label for="select-all">全选</label>
          <input
            type="checkbox"
            id="only-first"
            v-model="showOnlyFirst"
            @change="filterFirstRelease"
          />
          <label for="only-first">只看首发</label>
          <span class="data-total">数据总量：{{ totalItems }} 条</span>
          <button class="export-btn" @click="exportData">导出</button>
        </div>
      </div>

      <!-- 搜索结果区 -->
      <div class="search-results">
        <!-- 加载状态 -->
        <div v-if="isLoading" class="loading-indicator">
          <div class="spinner"></div>
          <span>正在加载...</span>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="searchError" class="error-message">
          <span>{{ searchError }}</span>
          <button @click="performSearch" class="retry-btn">重试</button>
        </div>

        <!-- 空结果 -->
        <!-- 逻辑：非加载状态 && 显示列表为空 && (处于搜索模式 OR 有搜索关键词) -->
        <div
          v-else-if="
            !isLoading && filteredNewsList.length === 0 && (isSearchMode || searchParams.topic)
          "
          class="no-results"
        >
          <span>未找到匹配的结果</span>
          <p>请尝试调整搜索条件或关键词</p>
        </div>

        <!-- 结果列表 -->
        <ul v-else class="result-list">
          <li class="result-item" v-for="item in filteredNewsList" :key="item.id">
            <input type="checkbox" v-model="item.selected" />
            <span v-if="item.isFirstRelease" class="first-release">首发</span>

            <div class="result-content">
              <h4 class="title">{{ item.title }}</h4>
              <p class="desc">{{ item.displayDesc }}</p>

              <div class="result-meta">
                <span v-if="item.source" class="source">●{{ item.source }}</span>
                <span v-if="item.displayTime" class="time">
                  {{ formatDateTime(item.displayTime) }}
                </span>
                <span v-if="item.location" class="location">{{
                  formatLocation(item.location)
                }}</span>
              </div>

              <div class="actions">
                <router-link
                  :to="`/data-service/news/${item.id}`"
                  class="view-detail"
                >
                  查看详情
                </router-link>
                <a
                  :href="item.displayUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="view-original"
                >
                  ②查看原文
                </a>
                <span class="neutral">中立</span>
                <button
                  type="button"
                  class="favorite-star-btn"
                  :class="{ active: isFavorited(item.id) }"
                  @click.prevent="toggleFavorite(item.id)"
                  :title="isFavorited(item.id) ? '取消收藏' : '收藏'"
                  :aria-label="isFavorited(item.id) ? '取消收藏' : '收藏'"
                >{{ isFavorited(item.id) ? '★' : '☆' }}</button>
                <a href="#" class="action-link">预警</a>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- 分页组件 -->
      <div class="pagination">
        <div class="pagination-info">
          <span>共{{ totalItems }}条</span>
          <select v-model="pageSize" @change="handlePageSizeChange">
            <option value="10">10条/页</option>
            <option value="20">20条/页</option>
            <option value="50">50条/页</option>
          </select>
        </div>
        <div class="pagination-controls">
          <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
            &lt;
          </button>
          <button
            v-for="page in visiblePages"
            :key="page"
            class="page-btn"
            :class="{ active: page === currentPage }"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>
          <button
            class="page-btn"
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
          >
            &gt;
          </button>
        </div>
        <div class="pagination-jump">
          <span>前往</span>
          <input
            type="number"
            v-model="jumpPage"
            :min="1"
            :max="totalPages"
            @keyup.enter="jumpToPage"
          />
          <span>页</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch, reactive } from 'vue'
import { API_PREFIX } from '@/config/api'

// 引入图标以避免报错 (如果在 main.js 注册了可删除)
import {
  Document,
  Bell,
  TrendCharts,
  User,
  Aim,
  Folder,
  SwitchButton,
  Search,
} from '@element-plus/icons-vue'

// 搜索参数
const searchParams = reactive({
  topic: '',
  mustInclude: '',
  anyInclude: '',
  needExclude: '',
  publishTime: '近一月',
  startTime: '',
  endTime: '',
  hitLocation: '全文',
  dataSource: '',
  language: '',
  site: '',
  page: 1,
  pageSize: 10,
  sortBy: 'pub_time',
  sortOrder: 'desc',
})

// 状态管理
const isLoading = ref(false)
const searchError = ref('')
const searchResults = ref([])
const newsList = ref([])
const isSearchMode = ref(false) // 核心状态：是否处于搜索结果展示模式
const favoriteNewsIds = ref([])

// 筛选后用于显示的最终列表
const filteredNewsList = ref([])

// 筛选选项
const timeRanges = ref([
  { label: '近一天', value: '近一天' },
  { label: '近一周', value: '近一周' },
  { label: '近一月', value: '近一月' },
  { label: '近三月', value: '近三月' },
  { label: '近一年', value: '近一年' },
])
const hitLocations = ref([
  { label: '全文', value: '全文' },
  { label: '标题', value: '标题' },
  { label: '摘要', value: '摘要' },
  { label: '正文', value: '正文' },
])

const dataSources = ref([])
const languages = ref([])
const sites = ref(['新闻网站', '博客', '社交媒体', '论坛'])

// 分页相关状态
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = ref(0)
const jumpPage = ref(1)
const selectAll = ref(false)
const showOnlyFirst = ref(false)

const isInitialized = ref(false)

const API_ENDPOINTS = {
  news: `${API_PREFIX}/dashboard/news`,
  search: `${API_PREFIX}/dashboard/search`,
  stats: `${API_PREFIX}/dashboard/stats`,
  favorites: `${API_PREFIX}/user/favorites`,
  favoriteToggle: `${API_PREFIX}/user/favorites/toggle`,
}

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

const syncFavoriteIdsFromList = (list) => {
  if (!Array.isArray(list) || list.length === 0) return
  const idsFromList = list
    .filter((item) => item && item.is_favorited && item.id !== undefined && item.id !== null)
    .map((item) => Number(item.id))
    .filter((id) => Number.isFinite(id))
  if (!idsFromList.length) return
  favoriteNewsIds.value = Array.from(new Set([...favoriteNewsIds.value, ...idsFromList]))
}

// ================== 数据处理核心逻辑 ==================

/**
 * 核心筛选与字段映射函数
 */
const filterFirstRelease = () => {
  // 根据 isSearchMode 决定使用哪份数据
  const rawList = isSearchMode.value ? searchResults.value : newsList.value

  const normalizedList = rawList.map((item) => ({
    ...item,
    id: item.id || Math.random().toString(36).substr(2, 9),
    title: item.title || '无标题',
    displayDesc: item.abstract || item.desc || '—',
    displayTime: item.pub_time || item.time,
    displayUrl: item.request_url || item.requestUrl || '#',
    isFirstRelease: item.is_first_release || item.isFirstRelease || false,
    selected: item.selected || false,
  }))

  if (showOnlyFirst.value) {
    filteredNewsList.value = normalizedList.filter((item) => item.isFirstRelease)
  } else {
    filteredNewsList.value = [...normalizedList]
  }

  updateSelectAllState()
}

/**
 * 加载分页列表数据（单接口 GET /api/dashboard/news）
 */
const loadPageData = async (page) => {
  isLoading.value = true
  searchError.value = ''

  isSearchMode.value = false

  const size = pageSize.value

  try {
    const url = new URL(API_ENDPOINTS.news)
    url.searchParams.set('page', String(page))
    url.searchParams.set('size', String(size))
    url.searchParams.set('sort_by', searchParams.sortBy || 'pub_time')
    url.searchParams.set('sort_order', searchParams.sortOrder || 'desc')

    const response = await fetch(url, {
      headers: { ...getAuthHeaders() },
    })
    if (!response.ok) throw new Error(`请求失败: ${response.status}`)
    const result = await response.json()

    const list = result.data || []
    newsList.value = list.map((item) => ({
      ...item,
      id: Number(item.id),
      is_favorited: !!item.is_favorited,
      selected: false,
    }))
    syncFavoriteIdsFromList(newsList.value)
    totalItems.value = result.total ?? 0
    searchResults.value = []

    filterFirstRelease()
  } catch (error) {
    console.error('加载初始数据失败：', error)
    searchError.value = '加载数据失败，请检查网络或重试'
    newsList.value = []
  } finally {
    isLoading.value = false
  }
}

/**
 * 重置搜索 - 恢复初始状态
 */
const resetSearch = async () => {
  isLoading.value = true

  // 1. 重置参数
  Object.assign(searchParams, {
    topic: '',
    mustInclude: '',
    anyInclude: '',
    needExclude: '',
    publishTime: '近一月',
    startTime: '',
    endTime: '',
    hitLocation: '全文',
    dataSource: '',
    language: '',
    site: '',
    page: 1,
    pageSize: 10,
    sortBy: 'pub_time',
    sortOrder: 'desc',
  })

  // 2. 清空状态并退出搜索模式
  isSearchMode.value = false
  searchResults.value = []
  searchError.value = ''
  currentPage.value = 1
  pageSize.value = 10
  jumpPage.value = 1

  // 3. 重新加载初始数据
  await loadPageData(1)

  scrollToTop()
}

// ================== 搜索逻辑 ==================

const performSearch = async () => {
  if (isLoading.value) return

  isLoading.value = true
  searchError.value = ''

  try {
    const params = {
      keyword:
        searchParams.topic || searchParams.mustInclude || searchParams.anyInclude || undefined,
      must_include: searchParams.mustInclude || undefined,
      any_include: searchParams.anyInclude || undefined,
      need_exclude: searchParams.needExclude || undefined,
      publish_time: searchParams.publishTime || undefined,
      start_time: searchParams.startTime || undefined,
      end_time: searchParams.endTime || undefined,
      hit_location: searchParams.hitLocation,
      data_source: searchParams.dataSource || undefined,
      language: searchParams.language || undefined,
      site: searchParams.site || undefined,
      page: searchParams.page,
      page_size: searchParams.pageSize,
      sort_by: searchParams.sortBy,
      sort_order: searchParams.sortOrder,
    }

    Object.keys(params).forEach((key) => {
      if (params[key] === '' || params[key] === undefined) delete params[key]
    })

    const response = await fetch(API_ENDPOINTS.search, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(params),
    })

    if (!response.ok) {
      throw new Error(`搜索失败: ${response.status} ${response.statusText}`)
    }

    const result = await response.json()

    // 【关键】切换为搜索模式
    isSearchMode.value = true
    searchResults.value = (result.data || []).map((item) => ({
      ...item,
      id: Number(item.id),
      is_favorited: !!item.is_favorited,
    }))
    syncFavoriteIdsFromList(searchResults.value)

    // 更新总数 (搜索结果的总数)
    totalItems.value = result.total || 0

    currentPage.value = result.page || searchParams.page
    pageSize.value = result.page_size || searchParams.pageSize
    searchParams.page = currentPage.value
    searchParams.pageSize = pageSize.value

    filterFirstRelease()
  } catch (error) {
    console.error('搜索失败:', error)
    searchError.value = error.message || '搜索失败，请稍后重试'
    searchResults.value = []
    totalItems.value = 0
    // 即使失败，保持在搜索模式以显示错误信息
    isSearchMode.value = true
    filterFirstRelease()
  } finally {
    isLoading.value = false
  }
}

// ================== 事件处理 ==================

const handleHitLocationChange = (val) => {
  searchParams.hitLocation = val
  performSearch()
}

const formatDateTime = (dateTime) => {
  if (!dateTime || dateTime === '—') return '—'
  try {
    const date = new Date(dateTime)
    if (isNaN(date.getTime())) return dateTime
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch (error) {
    return dateTime
  }
}

const formatLocation = (location) => {
  if (!location || location === '—') return '—'
  return `②${location}`
}

const setPublishTime = (range) => {
  searchParams.publishTime = range
  searchParams.startTime = ''
  searchParams.endTime = ''
  if (isInitialized.value) performSearch()
}

const onTimeRangeChange = () => {
  if (searchParams.startTime || searchParams.endTime) {
    searchParams.publishTime = ''
  }
  if (isInitialized.value) performSearch()
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    jumpPage.value = page
    searchParams.page = page
    scrollToTop()
    // 根据当前模式决定调用哪个加载函数
    if (isSearchMode.value) {
      performSearch()
    } else {
      loadPageData(page)
    }
  }
}

const jumpToPage = () => {
  const page = parseInt(jumpPage.value)
  if (page >= 1 && page <= totalPages.value) goToPage(page)
  else jumpPage.value = currentPage.value
}

const handlePageSizeChange = () => {
  currentPage.value = 1
  jumpPage.value = 1
  searchParams.page = 1
  searchParams.pageSize = pageSize.value
  scrollToTop()
  if (isSearchMode.value) {
    performSearch()
  } else {
    loadPageData(1)
  }
}

const scrollToTop = () => {
  nextTick(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  })
}

const handleSelectAllChange = () => {
  const isChecked = selectAll.value
  filteredNewsList.value.forEach((item) => {
    item.selected = isChecked
  })
}

const updateSelectAllState = () => {
  if (filteredNewsList.value.length > 0) {
    selectAll.value = filteredNewsList.value.every((item) => item.selected)
  } else {
    selectAll.value = false
  }
}

const exportData = () => {
  const selectedItems = filteredNewsList.value.filter((item) => item.selected)
  if (selectedItems.length === 0) {
    alert('请先选择要导出的数据')
    return
  }
  console.log('导出数据:', selectedItems)
  alert(`已选择 ${selectedItems.length} 条数据，导出功能待实现`)
}

const loadFilterOptions = async () => {
  try {
    const res = await fetch(API_ENDPOINTS.stats)
    if (res.ok) {
      const data = await res.json()
      const list = data.language_stats || []
      languages.value = list.map((x) => x.name).filter(Boolean)
    }
  } catch (e) {
    console.error('加载语言选项失败:', e)
  }
}

const handleFilterChange = () => {
  if (isInitialized.value) {
    performSearch()
  }
}

const isFavorited = (newsId) => favoriteNewsIds.value.includes(Number(newsId))

const loadFavorites = async () => {
  try {
    if (!localStorage.getItem('access_token')) return
    const res = await fetch(API_ENDPOINTS.favorites, {
      headers: { ...getAuthHeaders() }
    })
    if (!res.ok) return
    const data = await res.json()
    favoriteNewsIds.value = Array.isArray(data.news_ids)
      ? data.news_ids.map((id) => Number(id)).filter((id) => Number.isFinite(id))
      : []
  } catch (e) {
    console.error('加载收藏失败:', e)
  }
}

const toggleFavorite = async (newsId) => {
  try {
    if (!localStorage.getItem('access_token')) {
      alert('请先登录后再收藏')
      return
    }
    const res = await fetch(API_ENDPOINTS.favoriteToggle, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify({ news_id: newsId })
    })
    if (!res.ok) return
    const data = await res.json()
    const normalizedId = Number(newsId)
    if (data.favorited) {
      if (!favoriteNewsIds.value.includes(normalizedId)) {
        favoriteNewsIds.value = [...favoriteNewsIds.value, normalizedId]
      }
    } else {
      favoriteNewsIds.value = favoriteNewsIds.value.filter(id => id !== normalizedId)
    }
  } catch (e) {
    console.error('收藏操作失败:', e)
  }
}

// 监听 newsList 变化
watch(
  newsList,
  () => {
    if (!isSearchMode.value) {
      filterFirstRelease()
    }
  },
  { deep: true },
)

const totalPages = computed(() => {
  if (pageSize.value === 0) return 0
  return Math.ceil(totalItems.value / pageSize.value)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

onMounted(() => {
  jumpPage.value = currentPage.value
  loadFilterOptions()
  loadPageData(1)
  loadFavorites()
  isInitialized.value = true
})
</script>

<style scoped lang="less">
// 定义变量
@primary-color: #007bff;
@border-color: #ced4da;
@text-color: #333;
@text-light: #6c757d;
@bg-gray: #f8f9fa;
@bg-light: #e9ecef;
@danger-color: #dc3545;
@success-color: #28a745;
@warning-color: #ffc107;
@sidebar-width: 280px;

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.search-page {
  position: fixed;
  top: 60px; /* 导航栏高度 */
  left: 0;
  right: 0;
  bottom: 0;
  min-height: calc(100vh - 60px);
  background-color: #fff;
  overflow-y: auto; /* 内部滚动 */
}

// 左侧固定边栏
.left-sidebar {
  position: fixed; // 固定定位，悬浮在页面上方
  left: 0;
  top: 60px;
  bottom: 0;
  width: @sidebar-width;
  background-color: #f8f9fa;
  padding: 30px 25px;
  box-sizing: border-box;
  z-index: 1000; // 提高层级，确保悬浮在其他内容之上
  border-right: 1px solid #e9ecef;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1); // 添加阴影效果

  .search-input-group {
    margin-bottom: 40px;
    position: relative;

    .search-icon {
      position: absolute;
      left: 15px;
      top: 50%;
      transform: translateY(-50%);
      color: #667eea;
      font-weight: bold;
      font-size: 18px;
      z-index: 2;
    }

    .search-input {
      width: 100%;
      padding: 15px 15px 15px 45px;
      border: 1px solid @border-color;
      border-radius: 8px;
      font-size: 15px;
      box-sizing: border-box;
      background-color: #fff;

      &:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
      }

      &::placeholder {
        color: #999;
      }
    }
  }

  .language-model {
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    color: @text-color;
    font-size: 15px;
    padding: 12px 0;

    .model-icon {
      margin-right: 10px;
      color: #667eea;
      font-size: 18px;
    }
  }

  .add-theme-btn {
    width: 100%;
    padding: 15px;
    background-color: #667eea;
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 500;
    transition: all 0.3s;

    &:hover {
      background-color: #5a6fd8;
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
  }
}

// 右侧主内容区（占据整个视图）
.main-content {
  width: 95% !important; // 占据整个视图宽度
  padding: 0px 0px 0px 300px; // 左侧留出边栏空间，右侧进一步减少边距
  box-sizing: border-box;
  // 移除 overflow-y 和 max-height，使用浏览器滚动条
  margin-top: 0; // 移除margin-top，因为父容器已经处理了导航栏空间
  max-width: none !important;

  .search-condition {
    background-color: #fff;
    padding: 25px;
    border-radius: 8px;
    margin-bottom: 25px;
    border: 1px solid #e9ecef;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    width: 100%; // 确保搜索条件区域占满宽度

    h3 {
      margin-bottom: 20px;
      font-size: 20px;
      font-weight: 600;
      color: @text-color;
    }

    .condition-group {
      display: flex;
      gap: 20px;
      margin-bottom: 20px;
      flex-wrap: wrap;

      .condition-item {
        flex: 1;
        min-width: 250px;

        .tag {
          display: inline-block;
          padding: 4px 12px;
          border-radius: 6px;
          color: #fff;
          font-size: 13px;
          font-weight: 500;
          margin-bottom: 8px;

          &.must-include {
            background-color: #007bff;
          }

          &.any-include {
            background-color: #28a745;
          }

          &.need-exclude {
            background-color: #dc3545;
          }
        }

        input {
          width: 100%;
          padding: 12px;
          border: 1px solid @border-color;
          border-radius: 6px;
          font-size: 14px;
          box-sizing: border-box;

          &:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
          }

          &::placeholder {
            color: #999;
          }
        }
      }
    }

    .action-btns {
      display: flex;
      justify-content: flex-end;
      gap: 15px;

      .reset-btn {
        padding: 10px 20px;
        background-color: #fff;
        border: 1px solid @border-color;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s;

        &:hover {
          background-color: @bg-gray;
          border-color: #667eea;
        }
      }

      .search-btn {
        padding: 10px 20px;
        background-color: #667eea;
        color: #fff;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s;

        &:hover {
          background-color: #5a6fd8;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
      }
    }
  }

  .filter-section {
    margin-bottom: 25px;
    background-color: #fff;
    padding: 25px;
    border-radius: 8px;
    border: 1px solid #e9ecef;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    width: 100%; // 确保筛选区域占满宽度

    .filter-item {
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 15px;

      span {
        white-space: nowrap;
        font-weight: 500;
        color: @text-color;
        font-size: 14px;
      }

      button {
        padding: 8px 16px;
        border: 1px solid @border-color;
        border-radius: 6px;
        background-color: #fff;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s;

        &:hover {
          border-color: #667eea;
          color: #667eea;
        }

        &.active {
          background-color: #667eea;
          color: #fff;
          border-color: #667eea;
        }
      }

      select {
        padding: 8px 12px;
        border: 1px solid @border-color;
        border-radius: 6px;
        min-width: 140px;
        font-size: 14px;
        background-color: #fff;

        &:focus {
          outline: none;
          border-color: #667eea;
        }
      }

      input[type='text'] {
        padding: 8px 12px;
        border: 1px solid @border-color;
        border-radius: 6px;
        font-size: 14px;
        min-width: 180px;

        &:focus {
          outline: none;
          border-color: #667eea;
        }
      }

      input[type='checkbox'] {
        margin-right: 8px;
        transform: scale(1.2);
      }

      label {
        font-size: 14px;
        color: @text-color;
        cursor: pointer;
      }

      .data-total {
        margin-left: auto;
        color: @text-light;
        font-size: 14px;
        font-weight: 500;
      }

      .export-btn {
        padding: 8px 16px;
        background-color: #667eea;
        color: #fff;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s;

        &:hover {
          background-color: #5a6fd8;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
      }
    }
  }

  .search-results {
    width: 100%;
    min-height: 200px;

    .loading-indicator {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 60px 20px;
      color: @text-light;

      .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid @bg-gray;
        border-top-color: #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 15px;
      }

      span {
        font-size: 14px;
      }
    }

    .error-message {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 60px 20px;
      color: @danger-color;

      span {
        margin-bottom: 15px;
        font-size: 14px;
      }

      .retry-btn {
        padding: 8px 16px;
        background-color: #667eea;
        color: #fff;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;

        &:hover {
          background-color: #5a6fd8;
        }
      }
    }

    .no-results {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 60px 20px;
      color: @text-light;

      span {
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 10px;
      }

      p {
        font-size: 14px;
        margin: 0;
      }
    }
  }

  .result-list {
    width: 100%; // 确保结果列表占满宽度

    .result-item {
      border: 1px solid @bg-light;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      transition: all 0.3s;
      display: flex;
      align-items: flex-start;
      gap: 15px;
      width: 100%; // 确保每个结果项占满宽度

      &:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border-color: #667eea;
      }

      .first-release {
        background-color: #dc3545;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
        flex-shrink: 0;
      }

      .result-content {
        flex: 1;

        .title {
          font-weight: 600;
          font-size: 16px;
          color: @text-color;
          margin-bottom: 8px;
          line-height: 1.4;
        }

        .desc {
          margin: 8px 0 12px 0;
          color: @text-light;
          line-height: 1.5;
          font-size: 14px;
        }

        .result-meta {
          display: flex;
          align-items: center;
          gap: 15px;
          margin-bottom: 12px;
          font-size: 13px;

          .source {
            color: #667eea;
            font-weight: 500;
          }

          .time {
            color: @text-light;
          }

          .location {
            color: @text-light;
          }
        }

        .actions {
          display: flex;
          align-items: center;
          gap: 15px;

          a {
            color: #667eea;
            text-decoration: none;
            font-size: 13px;
            transition: color 0.3s;

            &:hover {
              text-decoration: underline;
            }
          }

          .neutral {
            color: @warning-color;
            font-size: 13px;
          }

          .favorite-star-btn {
            border: none;
            background: transparent;
            color: #94a3b8;
            font-size: 18px;
            cursor: pointer;
            opacity: 0.95;
            line-height: 1;
            padding: 0 2px;
            transition: color 0.2s ease, transform 0.2s ease, text-shadow 0.2s ease;
          }

          .favorite-star-btn:hover {
            color: #facc15;
            transform: scale(1.1);
          }

          .favorite-star-btn.active {
            color: #facc15;
            text-shadow: 0 0 8px rgba(250, 204, 21, 0.8);
          }
        }
      }
    }
  }

  // 分页组件样式
  .pagination {
    display: flex;
    justify-content: start;
    align-items: center;
    margin-top: 30px;
    padding: 20px 0;
    border-top: 1px solid #e9ecef;
    gap: 100px;

    .pagination-info {
      display: flex;
      align-items: center;
      gap: 15px;
      color: @text-light;
      font-size: 14px;

      select {
        padding: 6px 10px;
        border: 1px solid @border-color;
        border-radius: 4px;
        font-size: 14px;
        background-color: #fff;

        &:focus {
          outline: none;
          border-color: #667eea;
        }
      }
    }

    .pagination-controls {
      display: flex;
      align-items: center;
      gap: 5px;

      .page-btn {
        padding: 8px 12px;
        border: 1px solid @border-color;
        border-radius: 4px;
        background-color: #fff;
        color: @text-color;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s;
        min-width: 40px;

        &:hover:not(:disabled) {
          border-color: #667eea;
          color: #667eea;
        }

        &:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        &.active {
          background-color: #667eea;
          color: #fff;
          border-color: #667eea;
        }
      }
    }

    .pagination-jump {
      display: flex;
      align-items: center;
      gap: 8px;
      color: @text-light;
      font-size: 14px;

      input {
        width: 60px;
        padding: 6px 8px;
        border: 1px solid @border-color;
        border-radius: 4px;
        font-size: 14px;
        text-align: center;

        &:focus {
          outline: none;
          border-color: #667eea;
        }
      }
    }
  }
}
</style>

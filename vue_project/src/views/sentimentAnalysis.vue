<template>
  <!-- 舆情分析系统主容器 -->
  <div class="app-root">
    <!-- 顶部导航栏：包含搜索框、日期选择和时间范围控制 -->
    <nav class="top-nav">
      <div class="nav-left">
        <button
          class="history-toggle"
          @click="leftDrawerOpen = !leftDrawerOpen"
          title="搜索记录"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <span>搜索记录</span>
        </button>
        <div class="search-container">
          <input
            v-model="searchQuery"
            class="search-bar"
            placeholder="检索目标、事件、关键字..."
            @keyup.enter="handleSearch"
          />
          <button class="search-btn" @click="handleSearch" title="搜索">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
          </button>
        </div>
      </div>

      <div class="nav-right">
        <div class="control-group date-picker-wrap" @wheel.prevent="onDateWheel">
          <span class="control-label">起始日:</span>
          <el-date-picker
            v-model="startDate"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择日期"
            class="control-date-picker"
            popper-class="sentiment-date-picker-popper"
            :clearable="false"
          />
        </div>
        <div class="control-group">
          <span class="control-label">结束日:</span>
          <input class="control-input" :value="endDate" readonly />
        </div>
        <div class="control-group">
          <span class="control-label">视距:</span>
          <select class="control-select" v-model="timeRange">
            <option value="7d">近 7 天</option>
            <option value="30d">近 1 个月</option>
            <option value="90d">近 3 个月</option>
            <option value="365d">全年 (365天)</option>
            <option value="custom">自定义</option>
          </select>
          <input
            v-if="timeRange === 'custom'"
            v-model.number="customDays"
            type="number"
            min="1"
            max="365"
            class="control-input control-days-input"
            title="自定义天数"
          />
          <span v-if="timeRange === 'custom'" class="control-label">天</span>
        </div>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <div class="dashboard-layout">
      <!-- 宏观数据卡片区域：显示高危目标指数、情报截获短报、高频敏感词 -->
      <div class="macro-grid">
        <!-- 卡片1：高危目标指数 - 显示各国家/地区的负面舆情指数 -->
        <div class="macro-card">
          <div class="card-title">🚨 高危目标指数</div>
          <div class="target-indices">
            <span class="index-item negative">US (-28)</span>
            <span class="index-item negative">RU (-12)</span>
            <span class="index-item warning">JP (-5)</span>
          </div>
        </div>
        <!-- 卡片2：情报截获短报 - 显示最新的情报信息 -->
        <div class="macro-card">
          <div class="card-title">📡 情报截获短报</div>
          <div class="intel-brief">
            <div class="brief-item positive">● 南部基地卫星图像重构完成</div>
            <div class="brief-item normal">● 开源社区讨论热度上升 15%</div>
          </div>
        </div>
        <!-- 卡片3：高频敏感词 - 显示当前热门的敏感关键词标签 -->
        <div class="macro-card">
          <div class="card-title">🏷️ 高频敏感词</div>
          <div class="tags-container">
            <span class="tag tag-negative">#发射异常</span>
            <span class="tag tag-positive">#数据解密</span>
          </div>
        </div>
      </div>

      <!-- 图表容器：舆情指数折线图 -->
      <div class="chart-container">
        <div ref="chartRef" class="chart-wrapper"></div>
      </div>
    </div>

    <!-- 左侧栏：搜索记录 + 本次搜索结果 + AI 舆情分析 -->
    <div class="drawer drawer-left" :class="{ open: leftDrawerOpen }">
      <div class="drawer-header">
        <h2 class="drawer-title">搜索记录</h2>
        <button class="drawer-close" @click="leftDrawerOpen = false" title="关闭">✕</button>
      </div>
      <div class="drawer-content drawer-list">
        <p v-if="searchHistory.length === 0 && !searchLoading" class="drawer-empty">暂无搜索记录</p>
        <div
          v-for="(item, index) in searchHistory"
          :key="'h-' + index"
          class="search-history-item"
        >
          <span class="search-history-query">{{ item.query }}</span>
          <span class="search-history-time">{{ item.time }}</span>
        </div>
      </div>
      <!-- 本次搜索结果 -->
      <div v-if="searchLoading || searchResults.length > 0 || searchError" class="drawer-section">
        <h3 class="drawer-section-title">本次搜索结果</h3>
        <p v-if="searchLoading" class="drawer-empty">搜索中…</p>
        <p v-else-if="searchError" class="drawer-error">{{ searchError }}</p>
        <div v-else class="search-results-list">
          <div
            v-for="(item, index) in searchResults"
            :key="'r-' + item.id + '-' + index"
            class="search-result-item"
          >
            <div class="search-result-header">
              <span class="search-result-title" @click="goToNewsDetail(item.id)">{{ item.title || '无标题' }}</span>
              <button
                class="favorite-btn"
                :class="{ active: isFavorited(item.id) }"
                @click.stop="toggleFavorite(item.id)"
                :title="isFavorited(item.id) ? '取消收藏' : '收藏'"
                :aria-label="isFavorited(item.id) ? '取消收藏' : '收藏'"
              >{{ isFavorited(item.id) ? '★' : '☆' }}</button>
            </div>
            <span class="search-result-meta">{{ item.source || '' }} · {{ item.pub_time ? String(item.pub_time).slice(0, 10) : '' }}</span>
          </div>
        </div>
      </div>
      <!-- AI 舆情分析：需点击按钮再分析 -->
      <div v-if="searchResults.length > 0" class="drawer-section">
        <h3 class="drawer-section-title">AI 舆情分析</h3>
        <button
          type="button"
          class="ai-analyze-btn"
          :disabled="aiLoading"
          @click="runAiAnalysis"
        >
          {{ aiLoading ? '分析中…' : '进行 AI 分析' }}
        </button>
        <p v-if="aiError" class="drawer-error">{{ aiError }}</p>
        <div v-else-if="aiAnalysis" class="ai-analysis-content">{{ aiAnalysis }}</div>
      </div>
    </div>

    <!-- 侧边栏：点击数据点时显示详细信息 -->
    <div class="drawer" :class="{ open: drawerOpen }">
      <!-- 侧边栏头部：标题和关闭按钮 -->
      <div class="drawer-header">
        <h2 class="drawer-title" :style="{ color: selectedData?.color || '#0ea5e9' }" v-if="selectedData">
          情报下钻分析
        </h2>
        <button
          @click="drawerOpen = false"
          class="drawer-close"
          title="关闭"
        >✕</button>
      </div>
      <!-- 侧边栏内容：显示选中数据点的详细信息 -->
      <div v-if="selectedData">
        <!-- 数据点信息卡片：显示时间节点、分数和情绪状态 -->
        <div class="drawer-content" :style="{
          border: selectedData.score < 0 ? '4px solid rgba(255, 0, 0, 1)' : '4px solid rgba(14, 165, 233, 1)', // 负面警报红色，正面警报蓝色（和数字颜色一致）
          backgroundColor: 'transparent' // 背景透明
        }">
          <div class="drawer-meta">时间节点：{{ selectedData.date }}</div>
          <div class="drawer-score-section">
            <div class="score-value" :style="{ color: selectedData.color }">
              {{ selectedData.score }}
            </div>
            <div class="score-info">
              <div class="score-sentiment" :style="{
                backgroundColor: 'transparent',
                border: selectedData.score >= 0 ? '1px solid transparent' : 'none',
                padding: selectedData.score >= 0 ? '4px 8px' : '0',
                borderRadius: selectedData.score >= 0 ? '4px' : '0',
                color: selectedData.score >= 0 ? '#000' : 'var(--text-main)'
              }">{{ selectedData.sentiment }}</div>
              <div class="score-desc">复合算法计算结果</div>
            </div>
          </div>
        </div>

        <!-- 溯源新闻列表：显示与该数据点相关的新闻信息 -->
        <h4 class="news-title">溯源新闻列表：</h4>
        <div
          v-for="news in selectedData.news"
          :key="news.id"
          class="news-item"
          :class="{ 'news-item-positive': selectedData.score >= 0 }"
          :style="{
            borderLeftColor: selectedData.score < 0 ? 'rgba(255, 0, 0, 1)' : 'rgba(14, 165, 233, 1)' // 负面警报红色，正面警报蓝色（和时间节点框颜色一致）
          }"
        >
          <div class="news-title-text">{{ news.title }}</div>
          <div class="news-meta">
            类型标签:
            <span class="news-tag">{{ news.type }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { ElDatePicker } from 'element-plus'
import axios from 'axios'
import { API_PREFIX } from '@/config/api.js'

const router = useRouter()

// ==================== 响应式数据 ====================
const chartRef = ref(null)
const drawerOpen = ref(false)
const leftDrawerOpen = ref(false)
const selectedData = ref(null)
const timeRange = ref('30d')
const customDays = ref(30)
const startDate = ref('')
const searchQuery = ref('')
const searchHistory = ref([]) // 搜索记录：{ query, time }
const searchResults = ref([]) // 当前一次搜索的 10 条结果
const aiAnalysis = ref('')
const searchLoading = ref(false)
const aiLoading = ref(false)
const searchError = ref('')
const aiError = ref('')
const favoriteNewsIds = ref([])
let chartInstance = null

const PRESET_DAYS_MAP = {
  '7d': 7,
  '30d': 30,
  '90d': 90,
  '365d': 365,
}

const formatDateYmd = (date) => {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

// ==================== 数据生成 ====================
// 生成365天的模拟舆情数据，数值严格限制在 -30 到 70 之间
const fullData = computed(() => {
  const today = new Date()
  let base = new Date(today)
  base.setDate(today.getDate() - 364)
  let dates = []
  let values = []
  let currVal = 20

  for (let i = 0; i < 365; i++) {
    dates.push(formatDateYmd(base))

    let step = (Math.random() - 0.5) * 12
    currVal += step

    if (currVal > 70) currVal = 70 - Math.random() * 5
    if (currVal < -30) currVal = -30 + Math.random() * 5

    values.push(Math.round(currVal))
    base.setDate(base.getDate() + 1)
  }
  return { dates, values }
})

const endDate = computed(() => {
  const dates = fullData.value.dates
  return dates.length ? dates[dates.length - 1] : formatDateYmd(new Date())
})

// ==================== 监听器 ====================
const getCurrentRangeDays = () => {
  if (timeRange.value === 'custom') {
    const days = Number(customDays.value)
    return Number.isFinite(days) && days > 0 ? Math.min(365, Math.floor(days)) : 30
  }
  return PRESET_DAYS_MAP[String(timeRange.value)] || 30
}

const getRangeIndexes = () => {
  const dates = fullData.value.dates
  if (!dates.length) return { startIndex: 0, endIndex: 0, total: 0 }
  const endIndex = dates.length - 1
  const days = getCurrentRangeDays()
  const startIndex = Math.max(0, endIndex - days + 1)
  return { startIndex, endIndex, total: dates.length - 1 }
}

// ==================== 图表配置 ====================
const dataZoomRange = computed(() => {
  const { startIndex, endIndex, total } = getRangeIndexes()
  if (total <= 0) return { start: 0, end: 100 }
  return {
    start: (startIndex / total) * 100,
    end: (endIndex / total) * 100
  }
})

const zoomStartPercent = ref(0)
const zoomEndPercent = ref(100)
let isSyncingRange = false
watch([timeRange, customDays, fullData], () => {
  if (timeRange.value === 'custom') {
    const normalized = getCurrentRangeDays()
    if (normalized !== customDays.value) customDays.value = normalized
  }
  const dates = fullData.value.dates
  const { startIndex } = getRangeIndexes()
  isSyncingRange = true
  startDate.value = dates[startIndex] || formatDateYmd(new Date())
  const range = dataZoomRange.value
  zoomStartPercent.value = range.start
  zoomEndPercent.value = range.end
  isSyncingRange = false
}, { immediate: true })

// ECharts 图表配置选项
const chartOption = computed(() => {
  const start = zoomStartPercent.value
  const end = zoomEndPercent.value
  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: { backgroundColor: '#1e293b' }
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '18%',
      top: '8%',
      containLabel: true
    },
    yAxis: {
      type: 'value',
      min: -30,
      max: 70,
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } },
      axisLabel: { color: '#94a3b8' }
    },
    xAxis: {
      type: 'category',
      data: fullData.value.dates,
      axisLine: {
        onZero: true,
        symbol: ['none', 'arrow'],
        symbolSize: [10, 15],
        lineStyle: { color: '#ffffff', width: 2 }
      },
      axisLabel: { color: '#94a3b8' }
    },
    dataZoom: [
      {
        type: 'slider',
        start,
        end,
        bottom: 5,
        height: 36,
        textStyle: { color: '#94a3b8' },
        borderColor: 'rgba(255, 255, 255, 0.05)',
        fillerColor: 'rgba(14, 165, 233, 0.15)',
        dataBackground: {
          lineStyle: { color: '#334155', width: 1 },
          areaStyle: { color: '#0f172a', opacity: 0.8 }
        },
        selectedDataBackground: {
          lineStyle: { color: '#0ea5e9', width: 2 },
          areaStyle: { color: '#0ea5e9', opacity: 0.2 }
        },
        handleIcon: 'path://M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '80%',
        handleStyle: {
          color: '#0ea5e9',
          shadowBlur: 4,
          shadowColor: 'rgba(0,0,0,0.5)',
          borderWidth: 0
        }
      },
      {
        type: 'inside',
        start,
        end,
        zoomOnMouseWheel: false,
        moveOnMouseWheel: true
      }
    ],
    // 视觉映射：根据数值范围设置颜色（正数蓝色，负数红色）
    visualMap: {
      show: false,
      pieces: [
        { gt: 0, lte: 70, color: '#0ea5e9' }, // 正数：蓝色
        { gte: -30, lte: 0, color: '#ef4444' } // 负数：红色
      ]
    },
    // 数据系列配置：舆情指数折线图（关闭动画以提升帧率）
    series: [{
      name: '舆情指数',
      type: 'line',
      smooth: 0.3,
      symbolSize: 6,
      showSymbol: false,
      animation: false,
      emphasis: { focus: 'series', showSymbol: true },
      lineStyle: { width: 3 },
      areaStyle: { opacity: 0.15 },
      markPoint: {
        symbol: 'pin',
        symbolSize: 50,
        label: { color: '#fff', fontSize: 10 },
        data: [
          { type: 'max', name: '正面极值', itemStyle: { color: '#0ea5e9' } },
          { type: 'min', name: '负面极值', itemStyle: { color: '#ef4444' } }
        ]
      },
      data: fullData.value.values
    }]
  }
})

// ==================== 图表初始化 ====================
// 初始化 ECharts 图表实例，绑定事件监听器
const initChart = () => {
  if (!chartRef.value) {
    console.warn('图表容器未找到')
    return
  }

  try {
    chartInstance = echarts.init(chartRef.value)
    chartInstance.setOption(chartOption.value)

    // 绑定点击事件 - 确保事件正确绑定
    chartInstance.off('click') // 先移除可能存在的旧监听器
    chartInstance.off('datazoom')
    chartInstance.on('click', onChartClick)
    chartInstance.on('datazoom', onDataZoom)
  } catch (error) {
    console.error('图表初始化失败:', error)
  }
}

// ==================== 事件处理 ====================
// 图表点击事件：点击数据点时打开侧边栏显示详细信息
const onChartClick = (params) => {
  console.log('图表点击事件触发:', params)

  const date = params.componentType === 'markPoint' ? params.data.coord[0] : params.name
  const value = params.componentType === 'markPoint' ? params.data.coord[1] : params.value

  console.log('提取的数据:', { date, value })

  const isNegative = value < 0
  selectedData.value = {
    date: date,
    score: value,
    title: `${date} 舆情快报`,
    sentiment: isNegative ? '负面警报' : '正面趋势',
    color: isNegative ? '#ef4444' : '#0ea5e9',
    news: [
      { id: 1, title: isNegative ? '目标系统出现高危通报' : '重点技术方向监测到活跃动态', type: "核心新闻" },
      { id: 2, title: `开源社区讨论热度相比昨日变化 ${Math.abs(Math.round(value))}%`, type: "开源情报" }
    ]
  }

  console.log('设置 drawerOpen 前:', drawerOpen.value)
  drawerOpen.value = true
  console.log('设置 drawerOpen 后:', drawerOpen.value)
  console.log('侧边栏已打开，数据:', selectedData.value)

  // 强制触发更新
  nextTick(() => {
    console.log('nextTick 后 drawerOpen:', drawerOpen.value)
  })
}

// 起始日滚轮：上下滚动加减 1 天，边界限制在数据范围内
const onDateWheel = (e) => {
  const dates = fullData.value.dates
  if (!dates.length || !startDate.value) return
  let idx = dates.indexOf(startDate.value)
  if (idx === -1) idx = 0
  if (e.deltaY < 0) idx = Math.min(idx + 1, dates.length - 1)
  else idx = Math.max(idx - 1, 0)
  startDate.value = dates[idx]
}

watch(startDate, (val) => {
  const dates = fullData.value.dates
  if (!val || !dates.length || isSyncingRange) return
  let idx = dates.indexOf(val)
  if (idx === -1) idx = 0
  const endIndex = dates.length - 1
  const total = Math.max(1, endIndex)
  const days = Math.max(1, endIndex - idx + 1)
  if (timeRange.value !== 'custom') timeRange.value = 'custom'
  if (customDays.value !== days) customDays.value = days
  zoomStartPercent.value = (idx / total) * 100
  zoomEndPercent.value = 100
})

// 数据缩放事件：用户拖动时间条时仅更新百分比
const onDataZoom = () => {
  if (!chartInstance) return
  const option = chartInstance.getOption()
  const dz = option.dataZoom && option.dataZoom[0]
  if (dz && typeof dz.start === 'number' && typeof dz.end === 'number') {
    zoomStartPercent.value = dz.start
    zoomEndPercent.value = dz.end
  }
}

// 监听图表配置变化，重新设置选项并绑定事件（dataZoom 起止已由 chartOption 计算）
watch(chartOption, (newOption) => {
  if (chartInstance) {
    chartInstance.setOption(newOption, true)
    chartInstance.off('click')
    chartInstance.off('datazoom')
    chartInstance.on('click', onChartClick)
    chartInstance.on('datazoom', onDataZoom)
  }
}, { deep: true })

// ==================== 生命周期 ====================
// 组件挂载时初始化图表并绑定窗口大小变化监听
onMounted(() => {
  nextTick(() => {
    initChart()
    // 监听窗口大小变化
    window.addEventListener('resize', handleResize)
  })
  loadSearchHistory()
  loadFavorites()
})

// 组件卸载时清理图表实例和事件监听器
onUnmounted(() => {
  if (resizeTimer) clearTimeout(resizeTimer)
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})

// 处理窗口大小变化：节流后调整图表尺寸，减轻卡顿
let resizeTimer = null
const handleResize = () => {
  if (resizeTimer) return
  resizeTimer = setTimeout(() => {
    resizeTimer = null
    if (chartInstance) chartInstance.resize()
  }, 180)
}

// ==================== 搜索功能 ====================
const handleSearch = async () => {
  const q = searchQuery.value.trim()
  if (!q) return
  const now = new Date()
  const timeStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
  searchHistory.value = [{ query: q, time: timeStr }, ...searchHistory.value].slice(0, 50)
  searchResults.value = []
  aiAnalysis.value = ''
  searchError.value = ''
  aiError.value = ''
  leftDrawerOpen.value = true

  searchLoading.value = true
  aiAnalysis.value = ''
  aiError.value = ''
  try {
    const searchRes = await axios.post(
      `${API_PREFIX}/dashboard/search`,
      {
        keyword: q,
        page: 1,
        page_size: 10,
        hit_location: '全文'
      },
      { headers: getAuthHeaders() }
    )
    const list = searchRes.data?.data ?? searchRes.data?.data_list ?? []
    searchResults.value = Array.isArray(list)
      ? list.map((item) => ({
          ...item,
          id: Number(item.id),
          is_favorited: !!item.is_favorited,
        }))
      : []
    syncFavoriteIdsFromList(searchResults.value)
  } catch (e) {
    searchError.value = e?.response?.data?.detail || e?.message || '搜索失败'
    searchLoading.value = false
    return
  }
  searchLoading.value = false
  await saveSearchHistory(q)
}

// 用户点击「AI 舆情分析」按钮后再请求 AI
const runAiAnalysis = async () => {
  if (searchResults.value.length === 0) return
  const maxLen = 6000
  const parts = searchResults.value.slice(0, 10).map((item, i) => {
    const title = item.title || ''
    const abs = item.abstract || (item.body ? String(item.body).slice(0, 200) : '')
    return `[${i + 1}] ${title}\n${abs}`
  })
  let combinedText = parts.join('\n\n')
  if (combinedText.length > maxLen) combinedText = combinedText.slice(0, maxLen) + '…'
  aiLoading.value = true
  aiError.value = ''
  aiAnalysis.value = ''
  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch(`${API_PREFIX}/ai/analyze/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {})
      },
      body: JSON.stringify({ text: combinedText })
    })
    if (!res.ok || !res.body) {
      const text = await res.text()
      throw new Error(text || '流式分析失败')
    }
    const reader = res.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      const parts = buffer.split('\n\n')
      buffer = parts.pop() || ''
      for (const part of parts) {
        const line = part.trim()
        if (!line.startsWith('data:')) continue
        const payload = line.slice(5).trim()
        if (payload === '[DONE]') continue
        try {
          const jsonObj = JSON.parse(payload)
          if (jsonObj.delta) aiAnalysis.value += jsonObj.delta
          if (jsonObj.error) throw new Error(jsonObj.error)
        } catch (_) {
          // 非 JSON 块忽略
        }
      }
    }
  } catch (e) {
    aiError.value = e?.response?.data?.detail || e?.message || 'AI 分析请求失败'
  }
  aiLoading.value = false
}

const goToNewsDetail = (id) => {
  if (id) router.push(`/data-service/news/${id}`)
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

const loadSearchHistory = async () => {
  try {
    const hasToken = !!localStorage.getItem('access_token')
    if (!hasToken) return
    const res = await axios.get(`${API_PREFIX}/user/search-history`, { headers: getAuthHeaders() })
    const rows = res.data?.data || []
    if (Array.isArray(rows)) searchHistory.value = rows.map(r => ({ query: r.query, time: r.time }))
  } catch (_) {
    // 无需阻断主流程
  }
}

const saveSearchHistory = async (keyword) => {
  try {
    const hasToken = !!localStorage.getItem('access_token')
    if (!hasToken) return
    await axios.post(`${API_PREFIX}/user/search-history`, { keyword }, { headers: getAuthHeaders() })
  } catch (_) {
    // 无需阻断主流程
  }
}

const loadFavorites = async () => {
  try {
    const hasToken = !!localStorage.getItem('access_token')
    if (!hasToken) return
    const res = await axios.get(`${API_PREFIX}/user/favorites`, { headers: getAuthHeaders() })
    favoriteNewsIds.value = Array.isArray(res.data?.news_ids)
      ? res.data.news_ids.map((id) => Number(id)).filter((id) => Number.isFinite(id))
      : []
  } catch (_) {
    favoriteNewsIds.value = []
  }
}

const isFavorited = (newsId) => {
  return favoriteNewsIds.value.includes(Number(newsId))
}

const toggleFavorite = async (newsId) => {
  if (!newsId) return
  try {
    const hasToken = !!localStorage.getItem('access_token')
    if (!hasToken) {
      alert('请先登录后再收藏')
      return
    }
    const res = await axios.post(
      `${API_PREFIX}/user/favorites/toggle`,
      { news_id: newsId },
      { headers: getAuthHeaders() }
    )
    const favorited = !!res.data?.favorited
    const normalizedId = Number(newsId)
    if (favorited && !favoriteNewsIds.value.includes(normalizedId)) {
      favoriteNewsIds.value = [...favoriteNewsIds.value, normalizedId]
    } else if (!favorited) {
      favoriteNewsIds.value = favoriteNewsIds.value.filter(id => id !== normalizedId)
    }
  } catch (_) {
    // ignore
  }
}
</script>

<style scoped>
/* ==================== CSS 变量定义 ==================== */
:root {
  --bg-main: #0b1120; /* 主背景色 */
  --panel-bg: rgba(30, 41, 59, 0.7); /* 面板背景色 */
  --panel-border: rgba(255, 255, 255, 0.08); /* 面板边框色 */
  --text-main: #f8fafc; /* 主文本色 */
  --text-muted: #94a3b8; /* 次要文本色 */
  --color-pos: #0ea5e9; /* 正向情绪颜色（蓝色） */
  --color-neg: #ef4444; /* 负向情绪颜色（红色） */
  --color-warn: #f59e0b; /* 警告颜色（黄色） */
}

/* ==================== 主容器样式 ==================== */
.app-root {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: calc(100vh - 60px);
  margin: 0;
  padding: 0;
  background-color: var(--bg-main);
  background-image:
    radial-gradient(circle at 50% 0%, rgba(14, 165, 233, 0.08), transparent 50%),
    radial-gradient(circle at 100% 100%, rgba(239, 68, 68, 0.05), transparent 50%);
  color: var(--text-main);
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden;
}

/* ==================== 顶部导航栏样式 ==================== */
/* 顶部控制台：包含搜索框、日期选择和时间范围控制 */
.top-nav {
  height: 64px;
  background: var(--panel-bg);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--panel-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  position: relative;
  overflow: hidden;
}

/* 顶部导航栏科技感背景效果 */
.top-nav::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent,
    var(--color-pos) 20%,
    var(--color-pos) 80%,
    transparent
  );
  opacity: 0.6;
  animation: scanLine 3s linear infinite;
  will-change: transform;
  contain: layout paint;
}

@keyframes scanLine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  z-index: 1;
}

/* 搜索框容器：包含输入框和搜索按钮 */
.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-bar {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  color: var(--text-main);
  padding: 10px 50px 10px 18px;
  border-radius: 8px;
  width: 620px;
  transition: all 0.3s ease;
  outline: none;
  font-size: 0.9rem;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.06);
}

.search-bar::placeholder {
  color: #999; /* 与导航栏文字颜色一致 */
}

.search-bar:focus {
  border-color: var(--color-pos);
  box-shadow:
    inset 0 1px 2px rgba(0, 0, 0, 0.06),
    0 0 0 2px rgba(14, 165, 233, 0.15);
  background: rgba(255, 255, 255, 0.08);
}

/* 搜索按钮 */
.search-btn {
  position: absolute;
  right: 8px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.search-btn:hover {
  color: var(--color-pos);
  background: rgba(14, 165, 233, 0.1);
}

.search-btn:active {
  transform: scale(0.95);
}


@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 15px;
  position: relative;
  z-index: 1;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 500;
}

.control-input,
.control-select {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main);
  border: 1px solid var(--panel-border);
  padding: 8px 14px;
  border-radius: 6px;
  outline: none;
  color-scheme: dark;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.06);
}

.control-input:hover,
.control-select:hover {
  border-color: var(--color-pos);
  background: rgba(255, 255, 255, 0.08);
}

.control-input:focus,
.control-select:focus {
  border-color: var(--color-pos);
  box-shadow:
    inset 0 1px 2px rgba(0, 0, 0, 0.06),
    0 0 0 2px rgba(14, 165, 233, 0.15);
  background: rgba(255, 255, 255, 0.08);
}

.control-select option {
  background-color: rgba(255, 255, 255, 0.08);
  color: var(--text-main);
}

.date-picker-wrap {
  position: relative;
}
.control-date-picker {
  width: 160px;
}
.control-date-picker :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.06);
  color: var(--text-main);
}
.control-date-picker :deep(.el-input__wrapper:hover),
.control-date-picker :deep(.el-input__wrapper.is-focus) {
  border-color: var(--color-pos);
  background: rgba(255, 255, 255, 0.08);
}
.control-date-picker :deep(.el-input__inner) {
  color: var(--text-main);
}
.control-date-picker :deep(.el-input__suffix) {
  color: var(--text-muted);
}
.control-days-input {
  width: 88px;
  padding-left: 10px;
  padding-right: 10px;
}

/* ==================== 主内容区域布局 ==================== */
.dashboard-layout {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 124px);
  padding: 20px;
  gap: 20px;
  box-sizing: border-box;
}

/* ==================== 宏观数据卡片样式 ==================== */
/* 三个信息卡片：高危目标指数、情报截获短报、高频敏感词 */
.macro-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  min-height: 150px;
}

.macro-card {
  background: var(--panel-bg);
  backdrop-filter: blur(8px);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
}

.macro-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.22);
  border-color: rgba(255, 255, 255, 0.12);
}

.macro-card:nth-child(1)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--color-neg), transparent);
}

.macro-card:nth-child(2)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--color-pos), transparent);
}

.macro-card:nth-child(3)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--color-warn), transparent);
}

.card-title {
  font-size: 1.05rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--text-main);
  -webkit-text-stroke: 1px rgba(255, 255, 255, 0.35);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  font-family: 'Segoe UI', 'Inter', system-ui, sans-serif;
}

.target-indices {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.4rem;
  font-weight: 700;
}

.index-item {
  color: var(--color-neg);
  font-weight: 700;
  -webkit-text-stroke: 0.5px rgba(255, 255, 255, 0.25);
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
}

.index-item.negative {
  color: var(--color-neg);
}

.index-item.warning {
  color: var(--color-warn);
}

.intel-brief {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.brief-item {
  font-size: 1rem;
  line-height: 1.45;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.brief-item.positive {
  color: var(--color-pos);
}

.brief-item.normal {
  color: var(--text-main);
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.tag {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  -webkit-text-stroke: 0.5px rgba(255, 255, 255, 0.2);
}

.tag-negative {
  background: rgba(239, 68, 68, 0.25);
  color: var(--color-neg);
}

.tag-positive {
  background: rgba(14, 165, 233, 0.25);
  color: var(--color-pos);
}

/* ==================== 图表容器样式 ==================== */
/* 舆情指数折线图容器 */
.chart-container {
  flex: 1;
  background: var(--panel-bg);
  backdrop-filter: blur(8px);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  padding: 20px;
  min-height: 0;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.chart-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent,
    var(--color-pos) 50%,
    transparent
  );
  opacity: 0.3;
}

.chart-wrapper {
  width: 100%;
  height: 100%;
  contain: layout paint;
}

/* ==================== 侧边栏样式 ==================== */
/* 点击数据点时显示的详细信息侧边栏 */
.drawer {
  position: fixed;
  top: 124px;
  right: -420px;
  width: 400px;
  height: calc(100vh - 124px);
  background: var(--panel-bg);
  backdrop-filter: blur(12px);
  border-left: 1px solid var(--panel-border);
  box-shadow: -4px 0 16px rgba(0, 0, 0, 0.18);
  transition: right 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 2000;
  padding: 24px;
  box-sizing: border-box;
  overflow-y: auto;
}

.drawer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent,
    var(--color-pos) 50%,
    transparent
  );
  opacity: 0.5;
}

.drawer.open {
  right: 0;
}

/* 左侧抽屉：深色背景保证可读，与右侧样式对齐 */
.drawer-left {
  right: auto;
  left: -420px;
  background: rgba(15, 23, 42, 0.98);
  border-left: none;
  border-right: 1px solid rgba(14, 165, 233, 0.25);
  box-shadow: 4px 0 16px rgba(0, 0, 0, 0.18);
}
.drawer-left.open {
  left: 0;
  right: auto;
}
.drawer-left .drawer-title {
  color: #e2e8f0;
}
.drawer-left .drawer-section-title {
  color: #7dd3fc;
}

.history-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  color: var(--text-muted);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.history-toggle:hover {
  border-color: var(--color-pos);
  color: var(--color-pos);
  background: rgba(14, 165, 233, 0.08);
}

.drawer-list {
  max-height: 60vh;
  overflow-y: auto;
}
.drawer-empty {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0;
  padding: 16px 0;
}
.search-history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  margin-bottom: 8px;
  background: rgba(51, 65, 85, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 8px;
  font-size: 0.9rem;
}
.search-history-query {
  color: #e2e8f0;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.search-history-time {
  color: #94a3b8;
  font-size: 0.8rem;
  flex-shrink: 0;
}
.drawer-footer {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--panel-border);
}
.help-link {
  color: var(--color-pos);
  font-size: 0.9rem;
  text-decoration: none;
}
.help-link:hover {
  text-decoration: underline;
}

.drawer-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--panel-border);
}
.drawer-section-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-pos);
  margin: 0 0 12px 0;
}
.ai-analyze-btn {
  width: 100%;
  padding: 10px 16px;
  margin-bottom: 12px;
  background: rgba(14, 165, 233, 0.25);
  border: 1px solid var(--color-pos);
  border-radius: 8px;
  color: #e0f2fe;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.ai-analyze-btn:hover:not(:disabled) {
  background: rgba(14, 165, 233, 0.4);
  border-color: #38bdf8;
}
.ai-analyze-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.search-results-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 280px;
  overflow-y: auto;
}
.search-result-item {
  padding: 10px 12px;
  background: rgba(15, 23, 42, 0.9);
  border: 1px solid rgba(14, 165, 233, 0.35);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.search-result-item:hover {
  background: rgba(30, 58, 138, 0.6);
  border-color: var(--color-pos);
}
.search-result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.search-result-title {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #f8fafc;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}
.search-result-meta {
  font-size: 0.78rem;
  color: #cbd5e1;
}
.ai-analysis-content {
  font-size: 0.9rem;
  line-height: 1.65;
  color: #f1f5f9;
  white-space: pre-wrap;
  padding: 14px;
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(14, 165, 233, 0.35);
  border-radius: 10px;
  max-height: 320px;
  overflow-y: auto;
}
.drawer-error {
  color: #fca5a5;
  font-size: 0.9rem;
  margin: 0 0 8px 0;
  padding: 8px 0;
}
.favorite-btn {
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 1.05rem;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  opacity: 0.95;
  text-shadow: none;
  transition: color 0.2s ease, transform 0.2s ease, text-shadow 0.2s ease;
}
.favorite-btn:hover {
  color: #facc15;
  transform: scale(1.1);
}
.favorite-btn.active {
  color: #facc15;
  text-shadow: 0 0 8px rgba(250, 204, 21, 0.7);
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--panel-border);
}

.drawer-close {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  color: var(--text-muted);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: all 0.3s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-left: 15px;
}

.drawer-close:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
  color: #ef4444;
  transform: rotate(90deg);
  box-shadow: 0 1px 4px rgba(239, 68, 68, 0.25);
}

.drawer-title {
  color: var(--color-pos);
  font-size: 1.3rem;
  font-weight: 700;
  position: relative;
  flex: 1;
  margin: 0;
}

.drawer-title::after {
  content: '';
  position: absolute;
  bottom: -15px;
  left: 0;
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, var(--color-pos), transparent);
}

.drawer-content {
  background: rgba(0, 0, 0, 0.2);
  padding: 20px;
  border-radius: 12px;
  margin: 20px 0;
  border: 1px solid var(--panel-border);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 2px 8px rgba(0, 0, 0, 0.12);
  position: relative;
  overflow: hidden;
}

.drawer-content::before {
  display: none; /* 移除上边框的黑色线条 */
}

.drawer-meta {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.drawer-meta::before {
  content: '🕒';
  font-size: 0.8rem;
}

.drawer-score-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.score-value {
  font-size: 3.5rem;
  font-weight: 900;
  /* 去掉过强的发光效果，避免数值“溢出”视觉区域 */
  text-shadow: none;
  line-height: 1;
}

.score-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.score-sentiment {
  color: var(--text-main);
  font-weight: bold;
  font-size: 1.1rem;
}

.score-desc {
  color: var(--text-muted);
  font-size: 0.8rem;
}

.news-title {
  color: var(--text-main);
  margin-bottom: 15px;
  margin-top: 24px;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.news-title::before {
  content: '📰';
  font-size: 0.9rem;
}

.news-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--panel-border);
  padding: 14px;
  border-radius: 8px;
  margin-bottom: 12px;
  border-left: 3px solid;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.news-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: rgba(255, 0, 0, 1); /* 默认负面警报使用红色 */
  opacity: 0.6;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.6);
}

/* 正面趋势时，新闻项边框使用蓝色（和时间节点框颜色一致） */
.news-item-positive::before {
  background: rgba(14, 165, 233, 1); /* 正面警报使用蓝色，和数字颜色一致 */
  box-shadow: 0 0 10px rgba(14, 165, 233, 0.6);
}

.news-item:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.news-title-text {
  font-weight: bold;
  color: var(--text-main);
  line-height: 1.5;
  margin-bottom: 8px;
}

.news-meta {
  font-size: 0.8rem;
  margin-top: 8px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}

.news-tag {
  background: rgba(255, 255, 255, 0.1);
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.news-item:hover .news-tag {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.2);
}
</style>

<style>
/* 起始日日历弹层：淡蓝背景保证可读，与页面风格一致（无 scoped，弹层挂载在 body） */
.sentiment-date-picker-popper.el-picker-panel {
  background: #e0f2fe;
  border: 1px solid rgba(14, 165, 233, 0.35);
  border-radius: 12px;
  box-shadow: 0 10px 28px rgba(14, 165, 233, 0.2);
}
.sentiment-date-picker-popper .el-picker-panel__body-wrapper .el-picker-panel__body {
  background: transparent;
}
.sentiment-date-picker-popper .el-date-picker__header,
.sentiment-date-picker-popper .el-picker-panel__icon-btn,
.sentiment-date-picker-popper .el-date-table th {
  color: #0c4a6e;
  border-color: rgba(14, 165, 233, 0.2);
}
.sentiment-date-picker-popper .el-date-table td {
  color: #075985;
}
.sentiment-date-picker-popper .el-date-table td.available:hover {
  color: #0369a1;
}
.sentiment-date-picker-popper .el-date-table td .el-date-table-cell__text {
  color: inherit;
}
.sentiment-date-picker-popper .el-date-table td.current:not(.disabled) .el-date-table-cell__text {
  background: #0ea5e9;
  color: #fff;
  border-radius: 8px;
}
.sentiment-date-picker-popper .el-date-table td.today .el-date-table-cell__text {
  color: #0369a1;
  font-weight: 600;
}
.sentiment-date-picker-popper .el-picker-panel__icon-btn {
  color: #0c4a6e;
}
.sentiment-date-picker-popper .el-picker-panel__icon-btn:hover {
  color: #0ea5e9;
}
</style>

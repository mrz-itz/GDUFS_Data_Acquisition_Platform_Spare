<template>
  <div class="dashboard-container" ref="pageContainer">
    <!-- 顶部标题栏 -->
    <header class="dashboard-header">
      <h1>多语言新闻智库与涉华信息感知平台</h1>
      <div class="header-right">
        <span class="header-time">{{ currentTime }}</span>
        <div class="mode-selector" @click="toggleModeDropdown">
          <span class="mode-text">{{ currentMode === 'dark' ? '深色模式' : '浅色模式' }} ▾</span>
          <div class="mode-dropdown" v-if="showModeDropdown">
            <div
              class="mode-option"
              :class="{ active: currentMode === 'dark' }"
              @click.stop="changeMode('dark')"
            >
              深色模式
            </div>
            <div
              class="mode-option"
              :class="{ active: currentMode === 'light' }"
              @click.stop="changeMode('light')"
            >
              浅色模式
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 顶部数据卡片 -->
    <div class="top-cards">
      <div class="card-item" v-for="(item, index) in topData" :key="index">
        <!-- 四个角的高亮小方块 -->
        <span class="corner top-left"></span>
        <span class="corner top-right"></span>
        <span class="corner bottom-left"></span>
        <span class="corner bottom-right"></span>

        <img :src="item.icon" alt="item.label" class="card-icon" />
        <div class="card-content">
          <span class="card-number">{{ item.value }}</span>
          <span class="card-label">{{ item.label }}</span>
        </div>
      </div>
    </div>

    <!-- 中间内容区域 - 三列布局 -->
    <div class="content-wrapper">
      <!-- 左列：402px -->
      <div class="content-column">
        <!-- 上：全球热点新闻排行榜 -->
        <div class="panel panel-with-bg-image">
          <div class="title-with-decoration">
            <h3>全球热点新闻排行榜</h3>
            <img src="/src/assets/data_imgs/排行榜矩形.png" alt="" class="title-decoration" />
          </div>
          <div class="tabs-header">
            <div class="tabs">
              <span
                class="tab"
                :class="{ active: rankType === 'day' }"
                @click="changeRankType('day')"
                >日榜</span
              >
              <span
                class="tab"
                :class="{ active: rankType === 'week' }"
                @click="changeRankType('week')"
                >周榜</span
              >
              <span
                class="tab"
                :class="{ active: rankType === 'month' }"
                @click="changeRankType('month')"
                >月榜</span
              >
            </div>
            <div class="hotness-label">
              <img src="/src/assets/data_imgs/热度图标.png" alt="热度" class="hotness-icon" />
              <span>热度</span>
            </div>
          </div>
          <ul class="news-list">
            <li class="news-item" v-for="(news, index) in newsRankData" :key="index">
              <img
                :src="`/src/assets/data_imgs/新闻排行榜${index + 1}.png`"
                :alt="`排名${index + 1}`"
                class="rank-icon-img"
              />
              <span class="news-title">{{ news.title }}</span>
              <span class="news-hot">
                {{ news.hotValue }}
                <img
                  v-if="news.trend === 'up' || news.trend === '▲' || news.trend === '↑'"
                  src="/src/assets/data_imgs/上升绿色箭头.png"
                  alt="上升"
                  class="trend-icon"
                />
                <img
                  v-else-if="news.trend === 'down' || news.trend === '▼' || news.trend === '↓'"
                  src="/src/assets/data_imgs/下降红色箭头.png"
                  alt="下降"
                  class="trend-icon"
                />
              </span>
            </li>
          </ul>
        </div>
        <!-- 下：多语言新闻占比 -->
        <div class="panel panel-with-bg-image">
          <div class="title-with-decoration">
            <h3>多语言新闻占比</h3>
            <img src="/src/assets/data_imgs/新闻占比矩形.png" alt="" class="title-decoration" />
          </div>
          <!-- ECharts 环形图容器 -->
          <div ref="languageChart" class="chart-container">
            <div v-if="!languageChartLoaded" class="chart-skeleton">
              <div class="skeleton-shimmer"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 中列：865px -->
      <div class="content-column">
        <!-- 上：全球涉华影响力指数 -->
        <div class="panel panel-with-middle-bg">
          <div class="title-with-decoration">
            <h3>全球涉华影响力指数</h3>
            <img src="/src/assets/data_imgs/矩形影响力指数 .png" alt="" class="title-decoration" />
          </div>
          <div class="tabs">
            <span
              class="tab"
              :class="{ active: influenceTimeRange === '15d' }"
              @click="changeInfluenceTimeRange('15d')"
              >近15天</span
            >
            <span
              class="tab"
              :class="{ active: influenceTimeRange === '30d' }"
              @click="changeInfluenceTimeRange('30d')"
              >近30天</span
            >
            <span
              class="tab"
              :class="{ active: influenceTimeRange === '90d' }"
              @click="changeInfluenceTimeRange('90d')"
              >近90天</span
            >
            <span
              class="tab"
              :class="{ active: influenceTimeRange === '6m' }"
              @click="changeInfluenceTimeRange('6m')"
              >近半年</span
            >
            <span
              class="tab"
              :class="{ active: influenceTimeRange === '1y' }"
              @click="changeInfluenceTimeRange('1y')"
              >近1年</span
            >
          </div>
          <!-- ECharts 柱状图容器 -->
          <div ref="influenceChart" class="chart-container">
            <div v-if="!influenceChartLoaded" class="chart-skeleton">
              <div class="skeleton-shimmer"></div>
            </div>
          </div>
        </div>
        <!-- 下：舆论情感分析 -->
        <div class="panel panel-with-middle-bg">
          <div class="title-with-decoration">
            <h3>舆论情感分析</h3>
            <img src="/src/assets/data_imgs/矩形情感分析.png" alt="" class="title-decoration" />
          </div>
          <div class="tabs-with-legend">
            <div class="tabs">
              <span
                class="tab"
                :class="{ active: sentimentTimeRange === '1d' }"
                @click="changeSentimentTimeRange('1d')"
                >近1天</span
              >
              <span
                class="tab"
                :class="{ active: sentimentTimeRange === '15d' }"
                @click="changeSentimentTimeRange('15d')"
                >近15天</span
              >
              <span
                class="tab"
                :class="{ active: sentimentTimeRange === '30d' }"
                @click="changeSentimentTimeRange('30d')"
                >近30天</span
              >
              <span
                class="tab"
                :class="{ active: sentimentTimeRange === '90d' }"
                @click="changeSentimentTimeRange('90d')"
                >近90天</span
              >
              <span
                class="tab"
                :class="{ active: sentimentTimeRange === '6m' }"
                @click="changeSentimentTimeRange('6m')"
                >近半年</span
              >
              <span
                class="tab"
                :class="{ active: sentimentTimeRange === '1y' }"
                @click="changeSentimentTimeRange('1y')"
                >近1年</span
              >
            </div>
            <div class="sentiment-legend">
              <span class="legend-item">
                <span class="legend-color" style="background-color: #2ed573"></span>
                <span>正面</span>
              </span>
              <span class="legend-item">
                <span class="legend-color" style="background-color: #00e1ff"></span>
                <span>中立</span>
              </span>
              <span class="legend-item">
                <span class="legend-color" style="background-color: #ff6b81"></span>
                <span>负面</span>
              </span>
            </div>
          </div>
          <!-- ECharts 折线图容器 -->
          <div ref="sentimentChart" class="chart-container">
            <div v-if="!sentimentChartLoaded" class="chart-skeleton">
              <div class="skeleton-shimmer"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右列：402px，跨越两行 -->
      <div class="content-column">
        <!-- 信源分析（包含两个子面板） -->
        <div class="panel source-analysis-panel panel-with-long-bg">
          <div class="title-with-decoration">
            <h3>信源分析</h3>
            <img src="/src/assets/data_imgs/矩形 信源分析.png" alt="" class="title-decoration" />
          </div>
          <!-- 上部分：全球主要媒体 -->
          <div class="sub-panel">
            <h4>全球主要媒体</h4>
            <div class="media-list">
              <div
                v-for="(media, index) in mediaData"
                :key="index"
                class="media-list-item"
                :class="{ 'row-even': index % 2 === 1 }"
              >
                <div class="media-rank">
                  <img
                    v-if="index < 3"
                    :src="`/src/assets/data_imgs/信源分析排名${index + 1}.png`"
                    :alt="`排名${index + 1}`"
                    class="rank-icon"
                  />
                  <span v-else>{{ index + 1 }}</span>
                </div>
                <div class="media-name">{{ media.name }}</div>
                <div
                  class="media-score"
                  :class="{
                    'score-first': index === 0,
                    'score-second': index === 1,
                    'score-third': index === 2,
                  }"
                >
                  {{ media.score }}
                </div>
              </div>
            </div>
          </div>
          <!-- 下部分：信源类型分布 -->
          <div class="sub-panel">
            <h4 class="no-border-bottom">信源类型分布</h4>
            <!-- ECharts 饼图容器 -->
            <div ref="sourceTypeChart" class="chart-container">
              <div v-if="!sourceTypeChartLoaded" class="chart-skeleton">
                <div class="skeleton-shimmer"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 按需引入 ECharts，减少包体积
import * as echarts from 'echarts/core'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import axios from 'axios'
import { API_PREFIX } from '@/config/api'
import { ref, onMounted, onUnmounted, onActivated, nextTick } from 'vue'
import { useRoute } from 'vue-router'

// 注册必要的组件
echarts.use([
  BarChart,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  CanvasRenderer
])

const route = useRoute()
const pageContainer = ref(null)

/**
 * ===================================================================
 * 后端接口汇总（所有接口统一管理，方便查找和维护）
 * ===================================================================
 *
 * 【接口1】GET /api/dashboard/top-data
 *   用途：获取顶部四个卡片数据（新闻数、站点数、语种数、国家数）
 *   函数：getTopData()
 *
 * 【接口2】GET /api/dashboard/news-rank?type={day|week|month}
 *   用途：获取新闻排行榜数据
 *   函数：getNewsRankData(type)
 *   参数：type - 'day'(日榜) / 'week'(周榜) / 'month'(月榜)
 *
 * 【接口3】GET /api/dashboard/influence-index?timeRange={15d|30d|90d|6m|1y}
 *   用途：获取全球涉华影响力指数数据
 *   函数：getInfluenceData(timeRange)
 *   参数：timeRange - '15d'(近15天) / '30d'(近30天) / '90d'(近90天) / '6m'(近半年) / '1y'(近1年)
 *
 * 【接口4】GET /api/dashboard/media-source
 *   用途：获取全球主要媒体数据（信源分析-全球主要媒体）
 *   函数：getMediaData()
 *
 * 【接口5】GET /api/dashboard/language-ratio
 *   用途：获取多语言新闻占比数据
 *   函数：getLanguageRatioData()
 *
 * 【接口6】GET /api/dashboard/sentiment-analysis?timeRange={1d|15d|30d|90d|6m|1y}
 *   用途：获取舆论情感分析数据
 *   函数：getSentimentData(timeRange)
 *   参数：timeRange - '1d'(近1天) / '15d'(近15天) / '30d'(近30天) / '90d'(近90天) / '6m'(近半年) / '1y'(近1年)
 *
 * 【接口7】GET /api/dashboard/source-type
 *   用途：获取信源类型分布数据（信源分析-信源类型分布）
 *   函数：getSourceTypeData()
 *
 *
 * ===================================================================
 * 所有接口的详细说明、参数格式、返回数据格式请查看下方对应的函数注释
 * ===================================================================
 */

// ========================== 1. 状态定义 ==========================
// 顶部卡片数据
const topData = ref([])
// 新闻排行榜数据
const newsRankData = ref([])
// 排行榜类型（日/周/月）
const rankType = ref('day')
// 影响力指数相关
const influenceTimeRange = ref('15d')
const influenceTotal = ref(0)
const influenceIncrease = ref(0)
const influenceRate = ref(0)
// 媒体数据
const mediaData = ref([])
// 情感分析时间范围
const sentimentTimeRange = ref('1d')
// 当前时间
const currentTime = ref('')
// 模式选择（深色/浅色）
const currentMode = ref('dark')
const showModeDropdown = ref(false)

// ECharts 实例引用
const influenceChart = ref(null)
const languageChart = ref(null)
const sentimentChart = ref(null)
const sourceTypeChart = ref(null)

// ECharts 实例存储
let influenceChartInstance = null
let languageChartInstance = null
let sentimentChartInstance = null
let sourceTypeChartInstance = null

// 图表加载状态，用于显示骨架屏
const influenceChartLoaded = ref(false)
const languageChartLoaded = ref(false)
const sentimentChartLoaded = ref(false)
const sourceTypeChartLoaded = ref(false)

// 防抖函数
const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// 防抖的图表 resize 函数
const debouncedResizeCharts = debounce(() => {
  influenceChartInstance?.resize?.()
  languageChartInstance?.resize?.()
  sentimentChartInstance?.resize?.()
  sourceTypeChartInstance?.resize?.()
}, 300)

// 在组件顶部定义变量
let resizeObserver = null
let browserNavigationTimer = null

// 页面可见性变化处理器
const handleVisibilityChange = () => {
  if (!document.hidden) {
    // 页面变为可见时，强制更新图表
    setTimeout(() => {
      influenceChartInstance?.resize?.()
      languageChartInstance?.resize?.()
      sentimentChartInstance?.resize?.()
      sourceTypeChartInstance?.resize?.()
    }, 100)
  }
}

// 重置滚动位置到顶部
const resetScrollPosition = () => {
  // 重置window滚动位置
  window.scrollTo(0, 0)

  // 重置容器内部滚动位置
  nextTick(() => {
    if (pageContainer.value) {
      pageContainer.value.scrollTop = 0
    }
    // 再次确保window滚动位置为0
    window.scrollTo(0, 0)
  })
}

// 浏览器导航处理器
const handleBrowserNavigation = () => {
  // 清除之前的定时器
  if (browserNavigationTimer) {
    clearTimeout(browserNavigationTimer)
  }

  // 延迟执行，确保页面完全加载
  browserNavigationTimer = setTimeout(() => {
    // 重置滚动位置
    resetScrollPosition()

    initializeData()

    // 强制所有图表重新渲染
    if (influenceChartInstance) {
      influenceChartInstance.resize()
    }
    if (languageChartInstance) {
      languageChartInstance.resize()
    }
    if (sentimentChartInstance) {
      sentimentChartInstance.resize()
    }
    if (sourceTypeChartInstance) {
      sourceTypeChartInstance.resize()
    }
  }, 200)
}

// 设置容器大小观察器
const setupResizeObserver = () => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }

  const container = document.querySelector('.dashboard-container')
  if (container) {
    resizeObserver = new ResizeObserver((entries) => {
      for (let entry of entries) {
        setTimeout(() => {
          influenceChartInstance?.resize?.()
          languageChartInstance?.resize?.()
          sentimentChartInstance?.resize?.()
          sourceTypeChartInstance?.resize?.()
        }, 50)
      }
    })

    resizeObserver.observe(container)
  }
}

// ========================== 2. 后端接口配置 ==========================
const BASE_API = API_PREFIX

// ========================== 3. 后端接口调用（统一管理） ==========================
/**
 * 【接口1】获取顶部四个卡片数据（新闻数、站点数、语种数、国家数）
 *
 * 接口地址：GET /api/dashboard/top-data
 *
 * 请求参数：无
 *
 * 返回数据格式：
 * {
 *   code: 200,
 *   data: [
 *     { icon: '/src/assets/data_imgs/深色新闻图标.png', value: 34680, label: '新闻数' },
 *     { icon: '/src/assets/data_imgs/深色站点图标.png', value: 2495, label: '站点数' },
 *     { icon: '/src/assets/data_imgs/深色语种图标.png', value: 141, label: '语种数' },
 *     { icon: '/src/assets/data_imgs/深色国家图标.png', value: 141, label: '国家数' }
 *   ]
 * }
 */
const getTopData = async () => {
  try {
    // 调用统计接口
    const res = await axios.get(`${BASE_API}/dashboard/stats`)

    // 注意：后端返回直接是对象 { total_news: ..., ... }，不是 { code: 200, data: ... }
    // 除非你的 axios 拦截器做了处理。通常 FastAPI 直接返回数据。
    // 这里假设 axios 返回的 res.data 就是后端返回的 JSON。

    const data = res.data // 获取响应体

    // 映射数据
    topData.value = [
      {
        icon: '/src/assets/data_imgs/深色新闻图标.png',
        value: data.total_news || 0, // 映射 total_news
        label: '新闻数',
      },
      {
        icon: '/src/assets/data_imgs/深色站点图标.png',
        value: 2495, // 暂时保留模拟值，或者你可以请求后端增加 total_sites 字段
        label: '站点数',
      },
      {
        icon: '/src/assets/data_imgs/深色语种图标.png',
        value: data.total_languages || 0, // 映射 total_languages
        label: '语种数',
      },
      {
        icon: '/src/assets/data_imgs/深色国家图标.png',
        value: data.total_languages || 0, // 映射 total_languages (根据你的要求)
        label: '国家数',
      },
    ]
  } catch (error) {
    console.error('【接口1】获取顶部数据失败:', error)
    // 模拟数据（后端接口未就绪时使用，可删除）
    topData.value = [
      { icon: '/src/assets/data_imgs/深色新闻图标.png', value: 0, label: '新闻数' },
      { icon: '/src/assets/data_imgs/深色站点图标.png', value: 0, label: '站点数' },
      { icon: '/src/assets/data_imgs/深色语种图标.png', value: 0, label: '语种数' },
      { icon: '/src/assets/data_imgs/深色国家图标.png', value: 0, label: '国家数' },
    ]
  }
}

/**
 * 【接口2】获取新闻排行榜数据
 *
 * 接口地址：GET /api/dashboard/news-rank
 *
 * 请求参数：
 * @param {string} type - 排行榜类型，可选值：'day'(日榜) / 'week'(周榜) / 'month'(月榜)
 *
 * 返回数据格式：
 * {
 *   code: 200,
 *   data: [
 *     { title: '新闻标题', hotValue: '789.2w', trend: 'up' },  // trend: 'up'表示上升, 'down'表示下降
 *     { title: '新闻标题', hotValue: '612.7w', trend: 'down' },
 *     ... // 最多10条数据
 *   ]
 * }
 */
const getNewsRankData = async (type) => {
  try {
    const res = await axios.get(`${BASE_API}/dashboard/news-rank`, {
      params: { type },
    })
    const payload = res.data?.data ?? res.data
    if (Array.isArray(payload)) newsRankData.value = payload
  } catch (error) {
    console.error('【接口2】获取新闻排行榜失败:', error)
    // 模拟数据（后端接口未就绪时使用，可删除）
    newsRankData.value = [
      { title: '俄方目前只同美国就乌克兰问题进行谈判', hotValue: '789.2w', trend: 'up' },
      { title: '几内亚比绍过渡总统任命总理', hotValue: '612.7w', trend: 'down' },
      { title: '乌总统办公室主任辞职', hotValue: '600.9w', trend: 'down' },
      { title: '因简历存在虚假陈述罗马尼亚国防部长辞职', hotValue: '430.6w', trend: 'up' },
      { title: '美国拒发签证，伊朗将抵制男足世界杯抽签', hotValue: '210.4w', trend: 'up' },
      { title: '欧盟宣布对俄罗斯实施新一轮制裁措施', hotValue: '198.5w', trend: 'up' },
      { title: '日本央行维持超低利率政策不变', hotValue: '185.3w', trend: 'down' },
      { title: '法国总统访问非洲多国加强合作关系', hotValue: '172.8w', trend: 'up' },
      { title: '印度成功发射新型卫星进入预定轨道', hotValue: '165.2w', trend: 'up' },
      { title: '巴西经济数据显示第三季度增长放缓', hotValue: '158.6w', trend: 'down' },
    ]
  }
}

/**
 * 【接口3】获取全球涉华影响力指数数据
 *
 * 接口地址：GET /api/dashboard/influence-index
 *
 * 请求参数：
 * @param {string} timeRange - 时间范围，可选值：'15d'(近15天) / '30d'(近30天) / '90d'(近90天) / '6m'(近半年) / '1y'(近1年)
 *
 * 返回数据格式：
 * {
 *   code: 200,
 *   data: {
 *     total: 142687240,           // 总指数
 *     increase: 7240,             // 新增指数
 *     rate: 12,                   // 同比增幅（百分比）
 *     xAxis: ['1/6', '1/7', ...], // X轴日期数组，格式：'月/日'
 *     existingIndex: [6000000, 6500000, ...], // 已有指数数组（蓝色部分）
 *     newIndex: [1500000, 1600000, ...]       // 新增指数数组（绿色部分）
 *   }
 * }
 *
 * 注意：xAxis、existingIndex、newIndex 三个数组长度必须一致
 */
const getInfluenceData = async (timeRange) => {
  try {
    const res = await axios.get(`${BASE_API}/dashboard/influence-index`, {
      params: { timeRange },
    })
    const payload = res.data?.data ?? res.data
    if (payload && typeof payload === 'object') {
      const { total, increase, rate, xAxis, existingIndex, newIndex } = payload
      influenceTotal.value = total
      influenceIncrease.value = increase
      influenceRate.value = rate
      updateInfluenceChart(xAxis, existingIndex, newIndex)
    }
  } catch (error) {
    console.error('【接口3】获取影响力指数失败:', error)
    // 模拟数据（后端接口未就绪时使用，可删除）
    const mockData = getMockInfluenceData(timeRange)
    influenceTotal.value = mockData.total
    influenceIncrease.value = mockData.increase
    influenceRate.value = mockData.rate
    updateInfluenceChart(mockData.xAxis, mockData.existingIndex, mockData.newIndex)
  }
}

/**
 * 获取影响力指数模拟数据
 * @param {string} timeRange - 时间范围
 */
const getMockInfluenceData = (timeRange) => {
  // 生成密集的日期数据（从今天往前推，每天都有数据）
  const generateDailyDates = (days) => {
    const dates = []
    const today = new Date()
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(today)
      date.setDate(date.getDate() - i)
      const month = date.getMonth() + 1
      const day = date.getDate()
      dates.push(`${month}/${day}`)
    }
    return dates
  }

  // 生成对应的数值数据
  const generateValues = (baseValue, days, variation = 0.2) => {
    const values = []
    for (let i = 0; i < days; i++) {
      // 添加一些随机波动
      const variationAmount = baseValue * variation * (Math.random() - 0.5)
      values.push(Math.floor(baseValue + variationAmount))
    }
    return values
  }

  const mockDataMap = {
    '15d': {
      total: 142687240,
      increase: 7240,
      rate: 12,
      xAxis: generateDailyDates(15),
      totalValues: generateValues(8000000, 15, 0.15),
    },
    '30d': {
      total: 285374480,
      increase: 14480,
      rate: 15,
      xAxis: generateDailyDates(30),
      totalValues: generateValues(8000000, 30, 0.15),
    },
    '90d': {
      total: 856123440,
      increase: 43440,
      rate: 18,
      xAxis: generateDailyDates(90),
      totalValues: generateValues(7500000, 90, 0.2),
    },
    '6m': {
      total: 1712246880,
      increase: 86880,
      rate: 20,
      xAxis: generateDailyDates(180),
      totalValues: generateValues(7000000, 180, 0.25),
    },
    '1y': {
      total: 3424493760,
      increase: 173760,
      rate: 22,
      xAxis: generateDailyDates(365),
      totalValues: generateValues(6000000, 365, 0.3),
    },
  }

  const data = mockDataMap[timeRange] || mockDataMap['15d']
  const existingIndex = data.totalValues.map((val) => Math.floor(val * 0.8))
  const newIndex = data.totalValues.map((val, index) => val - existingIndex[index])

  return {
    total: data.total,
    increase: data.increase,
    rate: data.rate,
    xAxis: data.xAxis,
    existingIndex,
    newIndex,
  }
}

/**
 * 【接口4】获取全球主要媒体数据（信源分析-全球主要媒体）
 *
 * 接口地址：GET /api/dashboard/media-source
 *
 * 请求参数：无
 *
 * 返回数据格式：
 * {
 *   code: 200,
 *   data: [
 *     { name: '纽约时报', score: 89.1 },      // name: 媒体名称, score: 综合指数
 *     { name: '美国彭博新闻社', score: 89.1 },
 *     { name: '英国路透社', score: 89.1 },
 *     ... // 按综合指数从高到低排序，至少7条数据
 *   ]
 * }
 *
 * 注意：前3名的综合指数数字会显示为特殊颜色（第1名红色，第2名橙色，第3名黄色）
 */
const getMediaData = async () => {
  try {
    const res = await axios.get(`${BASE_API}/dashboard/media-source`)
    const payload = res.data?.data ?? res.data
    if (Array.isArray(payload)) mediaData.value = payload
  } catch (error) {
    console.error('【接口4】获取媒体数据失败:', error)
    // 模拟数据（后端接口未就绪时使用，可删除）
    mediaData.value = [
      { name: '纽约时报', score: 89.1 },
      { name: '美国彭博新闻社', score: 89.1 },
      { name: '英国路透社', score: 89.1 },
      { name: 'CNN', score: 89.1 },
      { name: 'BBC新闻', score: 89.1 },
      { name: '美国美联社', score: 89.1 },
      { name: '金融时报', score: 89.1 },
    ]
  }
}

/**
 * 【接口5】获取多语言新闻占比数据
 *
 * 接口地址：GET /api/dashboard/language-ratio
 *
 * 请求参数：无
 *
 * 返回数据格式：
 * {
 *   code: 200,
 *   data: [
 *     { name: '英语', value: 42 },      // name: 语言名称, value: 占比百分比（整数）
 *     { name: '法语', value: 21 },
 *     { name: '汉语', value: 7 },
 *     { name: '阿拉伯语', value: 15 },
 *     { name: '西班牙语', value: 15 }
 *   ]
 * }
 *
 * 注意：所有value的总和应该等于100
 */
const getLanguageRatioData = async () => {
  try {
    const res = await axios.get(`${BASE_API}/dashboard/language-ratio`)
    const payload = res.data?.data ?? res.data
    if (Array.isArray(payload)) updateLanguageChart(payload)
  } catch (error) {
    console.error('【接口5】获取语言占比失败:', error)
    // 模拟数据（后端接口未就绪时使用，可删除）
    updateLanguageChart([
      { name: '英语', value: 42 },
      { name: '法语', value: 21 },
      { name: '汉语', value: 7 },
      { name: '阿拉伯语', value: 15 },
      { name: '西班牙语', value: 15 },
    ])
  }
}

/**
 * 【接口6】获取舆论情感分析数据
 *
 * 接口地址：GET /api/dashboard/sentiment-analysis
 *
 * 请求参数：
 * @param {string} timeRange - 时间范围，可选值：'1d'(近1天) / '15d'(近15天) / '30d'(近30天) / '90d'(近90天) / '6m'(近半年) / '1y'(近1年)
 *
 * 返回数据格式：
 * {
 *   code: 200,
 *   data: {
 *     xAxis: ['2:00', '4:00', ...],           // X轴时间数组，格式根据timeRange不同而不同
 *     positive: [35000, 38000, ...],          // 正面情感数据数组（绿色折线）
 *     neutral: [25000, 28000, ...],           // 中立情感数据数组（蓝色折线）
 *     negative: [15000, 18000, ...]            // 负面情感数据数组（红色折线）
 *   }
 * }
 *
 * 注意：xAxis、positive、neutral、negative 四个数组长度必须一致
 *      - 1d: xAxis格式为时间点，如 ['2:00', '4:00', ..., '24:00']
 *      - 其他: xAxis格式为日期，如 ['1/6', '1/7', ...] 或根据实际需求
 */
const getSentimentData = async (timeRange) => {
  try {
    const res = await axios.get(`${BASE_API}/dashboard/sentiment-analysis`, {
      params: { timeRange },
    })
    const payload = res.data?.data ?? res.data
    if (payload && typeof payload === 'object') {
      const { xAxis, positive, neutral, negative } = payload
      updateSentimentChart(xAxis, positive, neutral, negative)
    }
  } catch (error) {
    console.error('【接口6】获取情感分析失败:', error)
    // 模拟数据（后端接口未就绪时使用，可删除）
    const mockData = getMockSentimentData(timeRange)
    updateSentimentChart(mockData.xAxis, mockData.positive, mockData.neutral, mockData.negative)
  }
}

/**
 * 【模拟数据函数】生成情感分析模拟数据
 * 仅用于开发测试，后端接口就绪后可删除此函数
 *
 * @param {string} timeRange - 时间范围
 * @returns {Object} 返回格式与接口6相同
 */
const getMockSentimentData = (timeRange) => {
  const mockDataMap = {
    '1d': {
      xAxis: [
        '2:00',
        '4:00',
        '6:00',
        '8:00',
        '10:00',
        '12:00',
        '14:00',
        '16:00',
        '18:00',
        '20:00',
        '22:00',
        '24:00',
      ],
      positive: [
        35000, 38000, 42000, 45000, 50000, 52000, 55000, 58000, 56000, 53000, 48000, 45000,
      ],
      neutral: [25000, 28000, 30000, 32000, 35000, 38000, 40000, 42000, 40000, 38000, 35000, 32000],
      negative: [15000, 18000, 20000, 18000, 15000, 12000, 10000, 8000, 10000, 12000, 15000, 18000],
    },
    '15d': {
      xAxis: ['10-9', '10-11', '10-13', '10-15', '10-17', '10-19', '10-21', '10-23'],
      positive: [75000, 80000, 85000, 90000, 88000, 92000, 87000, 85000],
      neutral: [60000, 65000, 70000, 75000, 72000, 78000, 70000, 68000],
      negative: [35000, 40000, 45000, 50000, 48000, 52000, 45000, 42000],
    },
    '30d': {
      xAxis: ['9-24', '9-28', '10-2', '10-6', '10-10', '10-14', '10-18', '10-22'],
      positive: [70000, 75000, 80000, 85000, 90000, 88000, 85000, 82000],
      neutral: [55000, 60000, 65000, 70000, 75000, 72000, 70000, 68000],
      negative: [30000, 35000, 40000, 45000, 50000, 48000, 45000, 42000],
    },
    '90d': {
      xAxis: ['7-26', '8-5', '8-15', '8-25', '9-4', '9-14', '9-24', '10-4', '10-14', '10-23'],
      positive: [60000, 65000, 70000, 75000, 80000, 85000, 90000, 88000, 85000, 82000],
      neutral: [50000, 55000, 60000, 65000, 70000, 75000, 80000, 78000, 75000, 72000],
      negative: [25000, 30000, 35000, 40000, 45000, 50000, 55000, 52000, 50000, 48000],
    },
    '6m': {
      xAxis: ['4-23', '5-23', '6-23', '7-23', '8-23', '9-23', '10-23'],
      positive: [50000, 60000, 70000, 80000, 90000, 85000, 82000],
      neutral: [40000, 50000, 60000, 70000, 80000, 75000, 72000],
      negative: [20000, 30000, 40000, 50000, 60000, 55000, 52000],
    },
    '1y': {
      xAxis: [
        '10-23(去年)',
        '11-23',
        '12-23',
        '1-23',
        '2-23',
        '3-23',
        '4-23',
        '5-23',
        '6-23',
        '7-23',
        '8-23',
        '9-23',
        '10-23',
      ],
      positive: [
        40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 85000, 82000,
      ],
      neutral: [
        30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 75000, 72000,
      ],
      negative: [
        15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 60000, 58000,
      ],
    },
  }

  return mockDataMap[timeRange] || mockDataMap['1d']
}

/**
 * 【接口7】获取信源类型分布数据（信源分析-信源类型分布）
 *
 * 接口地址：GET /api/dashboard/source-type
 *
 * 请求参数：无
 *
 * 返回数据格式：
 * {
 *   code: 200,
 *   data: [
 *     { name: '官方媒体', value: 32 },    // name: 信源类型名称, value: 占比百分比（整数）
 *     { name: '商业媒体', value: 28 },
 *     { name: '独立媒体', value: 12 },
 *     { name: '国际组织', value: 15 },
 *     { name: '其他', value: 15 }
 *   ]
 * }
 *
 * 注意：所有value的总和应该等于100
 */
const getSourceTypeData = async () => {
  try {
    const res = await axios.get(`${BASE_API}/dashboard/source-type`)
    const payload = res.data?.data ?? res.data
    if (Array.isArray(payload)) updateSourceTypeChart(payload)
  } catch (error) {
    console.error('【接口7】获取信源类型失败:', error)
    // 模拟数据（后端接口未就绪时使用，可删除）
    updateSourceTypeChart([
      { name: '官方媒体', value: 32 },
      { name: '商业媒体', value: 28 },
      { name: '独立媒体', value: 12 },
      { name: '国际组织', value: 15 },
      { name: '其他', value: 15 },
    ])
  }
}

// ========================== 4. 模拟数据生成函数（仅用于开发测试，后端接口就绪后可删除） ==========================

// -------------------------- 3. ECharts 图表初始化与更新 --------------------------
/**
 * 初始化影响力指数柱状图
 * @param {Array} xAxis - X轴数据
 * @param {Array} yAxis - Y轴数据
 */
const updateInfluenceChart = (xAxis, existingIndex, newIndex) => {
  if (!influenceChartInstance) {
    influenceChartInstance = echarts.init(influenceChart.value)
  }

  const option = {
    backgroundColor: 'transparent',
    animation: true, // 启用动画
    animationDuration: 1000, // 动画时长1000ms
    animationEasing: 'cubicOut', // 动画缓动效果
    animationDelayUpdate: function (idx) {
      // 让所有柱子同时更新动画，而不是依次动画
      return 0
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      backgroundColor: 'rgba(0, 150, 255, 0.9)',
      borderColor: 'rgba(0, 150, 255, 1)',
      borderWidth: 1,
      borderRadius: 4,
      textStyle: {
        color: '#fff',
        fontSize: 14,
        fontFamily: 'Microsoft Yahei',
      },
      formatter: function (params) {
        // 堆叠柱状图，params是数组，包含两个系列的数据
        let existing = 0
        let newVal = 0
        params.forEach((param) => {
          if (param.seriesName === '已有指数') {
            existing = param.value || 0
          } else if (param.seriesName === '新增指数') {
            newVal = param.value || 0
          }
        })
        const total = existing + newVal
        const rate = existing > 0 ? ((newVal / existing) * 100).toFixed(0) : 0
        return `总: ${total.toLocaleString()}<br/>增: ${newVal.toLocaleString()}<br/>同比增幅: ${rate}%`
      },
    },
    legend: {
      data: ['已有指数', '新增指数'],
      top: 0,
      right: 0,
      textStyle: {
        color: '#00e1ff',
        fontSize: 14,
        fontFamily: 'Microsoft Yahei',
      },
    },
    xAxis: {
      type: 'category',
      data: xAxis,
      axisLine: { lineStyle: { color: '#00e1ff' } },
      axisLabel: {
        color: '#00e1ff',
        fontSize: 14,
        fontFamily: 'Microsoft Yahei',
        formatter: function (value, index) {
          // 只显示第一个、最后一个，以及每隔一个显示的日期（隐藏中间的）
          // 对于15天：显示索引0, 2, 4, 6, 8, 10, 12, 14（每隔一个）
          // 对于30天：显示索引0, 2, 4, 6, ... 28（每隔一个）
          // 对于90天及以上：显示索引0, 最后一个，以及中间的某些
          const total = xAxis.length
          if (total <= 15) {
            // 15天以内：每隔一个显示
            return index % 2 === 0 ? value : ''
          } else if (total <= 30) {
            // 30天：每隔一个显示
            return index % 2 === 0 ? value : ''
          } else {
            // 90天及以上：显示第一个、最后一个，以及中间的某些
            if (index === 0 || index === total - 1) {
              return value
            }
            // 根据总数量决定显示间隔
            const interval = Math.ceil(total / 10) // 最多显示10个标签
            return index % interval === 0 ? value : ''
          }
        },
      },
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#00e1ff' } },
      axisLabel: {
        color: '#00e1ff',
        fontSize: 14,
        fontFamily: 'Microsoft Yahei',
      },
      splitLine: { lineStyle: { color: 'rgba(0, 225, 255, 0.35)' } },
    },
    series: [
      {
        name: '已有指数',
        type: 'bar',
        stack: 'total',
        data: existingIndex,
        itemStyle: {
          color: 'rgba(23, 218, 252, 1)', // 蓝色
          borderRadius: [0, 0, 0, 0], // 底部没有圆角，因为上面有绿色部分
        },
        barWidth: 15, // 固定宽度15px
        animationDelay: function (idx) {
          // 让所有柱子同时开始动画
          return 0
        },
        animationDelayUpdate: function (idx) {
          // 确保更新时也同步
          return 0
        },
      },
      {
        name: '新增指数',
        type: 'bar',
        stack: 'total', // 堆叠，确保两个系列黏在一起
        data: newIndex,
        itemStyle: {
          color: '#2ed573', // 纯绿色
          borderRadius: [9, 9, 0, 0], // 顶部圆角9px
        },
        barWidth: 15, // 固定宽度15px
        animationDelay: function (idx) {
          // 让所有柱子同时开始动画，与已有指数同步
          return 0
        },
        animationDelayUpdate: function (idx) {
          // 确保更新时也同步，与已有指数一起从底部向上过渡
          return 0
        },
      },
    ],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true,
    },
  }

  influenceChartInstance.setOption(option)
}

/**
 * 初始化多语言占比环形图
 * @param {Array} data - 语言占比数据
 */
const updateLanguageChart = (data) => {
  // 懒加载：等待 DOM 准备好
  if (!languageChart.value) {
    return
  }

  if (!languageChartInstance) {
    languageChartInstance = echarts.init(languageChart.value)
  }

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      show: false, // 禁用tooltip
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: {
        color: '#00e1ff',
        fontSize: 14,
        fontFamily: 'Microsoft Yahei',
      },
      itemGap: 12,
      // 图例图标使用圆形而不是圆角矩形
      icon: 'circle',
      formatter: function (name) {
        const item = data.find((d) => d.name === name)
        return item ? `${name} ${item.value}%` : name
      },
    },
    series: [
      {
        name: '语言占比',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['30%', '50%'], // 往左移，center从默认的50%改为30%
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#0a0e27',
          borderWidth: 2,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: false,
          },
        },
        labelLine: { show: false },
        data: data,
      },
    ],
    color: ['#00e1ff', '#7b61ff', '#ff6b81', '#ffa502', '#2ed573'],
  }

  languageChartInstance.setOption(option)
}

/**
 * 初始化情感分析折线图
 * @param {Array} xAxis - X轴数据
 * @param {Array} positive - 正面数据
 * @param {Array} neutral - 中立数据
 * @param {Array} negative - 负面数据
 */
const updateSentimentChart = (xAxis, positive, neutral, negative) => {
  // 懒加载：等待 DOM 准备好
  if (!sentimentChart.value) {
    return
  }

  if (!sentimentChartInstance) {
    sentimentChartInstance = echarts.init(sentimentChart.value)
  }

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
      backgroundColor: 'rgba(0, 150, 255, 0.9)',
      borderColor: 'rgba(0, 150, 255, 1)',
      borderWidth: 1,
      borderRadius: 4,
      textStyle: {
        color: '#fff',
        fontSize: 14,
        fontFamily: 'Microsoft Yahei',
      },
      formatter: function (params) {
        let result = params[0].name + '<br/>'
        params.forEach(function (item) {
          result += item.marker + item.seriesName + ': ' + item.value.toLocaleString() + '<br/>'
        })
        return result
      },
    },
    legend: {
      show: false, // 隐藏ECharts的图例，使用自定义图例
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%', // 增加顶部间距，让图表更高
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: xAxis,
      axisLine: { lineStyle: { color: '#00e1ff' } },
      axisLabel: { color: '#00e1ff' },
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#00e1ff' } },
      axisLabel: { color: '#00e1ff' },
      splitLine: {
        lineStyle: { color: 'rgba(0, 225, 255, 0.35)' },
        show: true,
      },
      // 使用interval精确控制分割线间隔，避免与最大值标签重叠
      interval: 10000, // 每10000一个分割线
      splitNumber: 5, // 保持分割线数量
      min: function (value) {
        // 设置最小值，让图表底部留一点空间但不超出
        const range = value.max - value.min
        return Math.max(0, value.min - range * 0.05)
      },
      max: function (value) {
        // 设置最大值，让图表顶部留一点空间但不超出
        // 确保最大值不是整数倍，避免分割线和最大值标签重叠
        const range = value.max - value.min
        const maxValue = value.max + range * 0.05
        // 向上取整到最近的10000的倍数，然后增加2000，确保分割线不会在最大值处
        const roundedMax = Math.ceil(maxValue / 10000) * 10000
        return roundedMax + 2000 // 增加2000，确保最大值标签和分割线不重叠
      },
    },
    series: [
      {
        name: '正面',
        type: 'line',
        data: positive,
        lineStyle: { color: '#2ed573' },
        itemStyle: { color: '#2ed573' },
        smooth: true,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(46, 213, 115, 0.8)' }, // 绿色，80%透明度，更深
              { offset: 1, color: 'rgba(46, 213, 115, 0)' }, // 完全透明
            ],
          },
        },
      },
      {
        name: '中立',
        type: 'line',
        data: neutral,
        lineStyle: { color: '#00e1ff' },
        itemStyle: { color: '#00e1ff' },
        smooth: true,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(0, 225, 255, 0.8)' }, // 蓝色，80%透明度，更深
              { offset: 1, color: 'rgba(0, 225, 255, 0)' }, // 完全透明
            ],
          },
        },
      },
      {
        name: '负面',
        type: 'line',
        data: negative,
        lineStyle: { color: '#ff6b81' },
        itemStyle: { color: '#ff6b81' },
        smooth: true,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(255, 107, 129, 0.8)' }, // 红色，80%透明度，更深
              { offset: 1, color: 'rgba(255, 107, 129, 0)' }, // 完全透明
            ],
          },
        },
      },
    ],
  }

  sentimentChartInstance.setOption(option)
}

/**
 * 初始化信源类型分布饼图
 * @param {Array} data - 信源类型数据
 */
const updateSourceTypeChart = (data) => {
  // 懒加载：等待 DOM 准备好
  if (!sourceTypeChart.value) {
    return
  }

  if (!sourceTypeChartInstance) {
    sourceTypeChartInstance = echarts.init(sourceTypeChart.value)
  }

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      show: false, // 禁用tooltip
    },
    legend: {
      show: false, // 隐藏图例
    },
    series: [
      {
        name: '信源类型',
        type: 'pie',
        radius: ['30%', '60%'],
        center: ['50%', '50%'], // 居中显示
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 0, // 改为0，使用普通环形图而不是圆角环形图
          borderColor: '#0a0e27',
          borderWidth: 2,
        },
        label: {
          show: true,
          color: '#fff',
          fontSize: 12, // 字体小一点
          fontFamily: 'Microsoft Yahei',
          formatter: '{b}: {c}%', // 显示名称和百分比
          overflow: 'none', // 不截断，确保显示全
          width: 100, // 设置标签宽度，确保显示全
        },
        labelLine: {
          show: true,
          length: 15,
          length2: 10,
          lineStyle: {
            color: '#00e1ff',
            width: 1,
          },
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
          },
        },
        data: data,
      },
    ],
    color: ['#00e1ff', '#7b61ff', '#ff6b81', '#ffa502', '#2ed573'],
  }

  sourceTypeChartInstance.setOption(option)
}

// ========================== 6. 事件处理函数 ==========================
/**
 * 切换新闻排行榜类型（日榜/周榜/月榜）
 * 触发接口2的调用
 *
 * @param {string} type - 排行榜类型：'day'(日榜) / 'week'(周榜) / 'month'(月榜)
 */
const changeRankType = (type) => {
  rankType.value = type
  getNewsRankData(type) // 调用接口2
}

/**
 * 切换影响力指数时间范围
 * 触发接口3的调用
 *
 * @param {string} timeRange - 时间范围：'15d'(近15天) / '30d'(近30天) / '90d'(近90天) / '6m'(近半年) / '1y'(近1年)
 */
const changeInfluenceTimeRange = (timeRange) => {
  influenceTimeRange.value = timeRange
  getInfluenceData(timeRange) // 调用接口3
}

/**
 * 切换情感分析时间范围
 * 触发接口6的调用
 *
 * @param {string} timeRange - 时间范围：'1d'(近1天) / '15d'(近15天) / '30d'(近30天) / '90d'(近90天) / '6m'(近半年) / '1y'(近1年)
 */
const changeSentimentTimeRange = (timeRange) => {
  sentimentTimeRange.value = timeRange
  getSentimentData(timeRange) // 调用接口6
}

// ========================== 7. UI交互函数 ==========================
/**
 * 切换模式下拉菜单显示/隐藏
 */
const toggleModeDropdown = () => {
  showModeDropdown.value = !showModeDropdown.value
}

/**
 * 切换深色/浅色模式
 *
 * @param {string} mode - 模式：'dark'(深色) / 'light'(浅色)
 */
const changeMode = (mode) => {
  currentMode.value = mode
  showModeDropdown.value = false
  // 这里可以添加切换主题的逻辑
  // 例如：document.body.classList.toggle('light-mode', mode === 'light')
}

/**
 * 点击外部关闭下拉菜单
 */
const handleClickOutside = (event) => {
  const modeSelector = event.target.closest('.mode-selector')
  if (!modeSelector && showModeDropdown.value) {
    showModeDropdown.value = false
  }
}

/**
 * 更新当前时间显示
 */
const updateCurrentTime = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hour = String(now.getHours()).padStart(2, '0')
  const minute = String(now.getMinutes()).padStart(2, '0')
  const second = String(now.getSeconds()).padStart(2, '0')
  currentTime.value = `${year}年${month}月${day}日 ${hour}时${minute}分${second}秒`
}

// ========================== 8. 生命周期钩子 ==========================
/**
 * 组件挂载时初始化所有数据
 * 调用所有后端接口获取数据
 */
// 在组件挂载时初始化
onMounted(() => {
  // 禁用浏览器的自动滚动恢复
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual'
  }

  // 重置滚动位置
  resetScrollPosition()

  initializeData()
  bindEventListeners()
  hasInitialized.value = true

  // 设置各种监听器
  setupResizeObserver()
  document.addEventListener('visibilitychange', handleVisibilityChange)
  window.addEventListener('popstate', handleBrowserNavigation)

  // 使用nextTick确保DOM已渲染后再重置一次
  nextTick(() => {
    resetScrollPosition()
  })
})

// 添加一个标志来追踪是否已经初始化
const hasInitialized = ref(false)

// 提取初始化逻辑到单独函数
const initializeData = async () => {
  // 调用所有接口获取数据
  await Promise.allSettled([
    getTopData(),
    getNewsRankData(rankType.value),
    getInfluenceData(influenceTimeRange.value),
    getMediaData(),
    getLanguageRatioData(),
    getSentimentData(sentimentTimeRange.value),
    getSourceTypeData(),
  ])

  // 初始化时间
  updateCurrentTime()

  // 标记已初始化
  hasInitialized.value = true
}

// 事件监听器绑定函数
// 事件监听器绑定函数
const bindEventListeners = () => {
  // 避免重复绑定：先检查是否已经存在定时器
  if (window.timeIntervalId) {
    clearInterval(window.timeIntervalId)
  }

  // 启动时间更新定时器
  window.timeIntervalId = setInterval(updateCurrentTime, 1000)

  // 监听窗口大小变化，自适应图表
  const resizeHandler = () => {
    setTimeout(() => {
      influenceChartInstance?.resize()
      languageChartInstance?.resize()
      sentimentChartInstance?.resize()
      sourceTypeChartInstance?.resize()
    }, 100)
  }
  window.addEventListener('resize', resizeHandler)

  // 添加点击外部关闭下拉菜单的事件监听
  document.addEventListener('click', handleClickOutside)

  // 将清理函数存储起来
  window.unbindEvents = () => {
    if (window.timeIntervalId) {
      clearInterval(window.timeIntervalId)
      delete window.timeIntervalId
    }
    window.removeEventListener('resize', resizeHandler)
    document.removeEventListener('click', handleClickOutside)
  }
}

// 重要：使用 onActivated 钩子确保浏览器前进/后退时也能重新初始化
onActivated(() => {
  // 重置滚动位置
  resetScrollPosition()

  // 确保每次激活时都正确处理
  setTimeout(() => {
    initializeData()
    bindEventListeners()
    hasInitialized.value = true

    // 强制图表更新
    nextTick(() => {
      setTimeout(() => {
        influenceChartInstance?.resize?.()
        languageChartInstance?.resize?.()
        sentimentChartInstance?.resize?.()
        sourceTypeChartInstance?.resize?.()
        // 再次确保滚动位置重置
        resetScrollPosition()
      }, 100)
    })
  }, 50)
})

// 一次性清理函数
const cleanup = () => {
  // 清理定时器
  if (window.timeIntervalId) {
    clearInterval(window.timeIntervalId)
    delete window.timeIntervalId
  }

  // 清理事件监听器
  if (window.unbindEvents) {
    window.unbindEvents()
    delete window.unbindEvents
  }

  // 销毁ECharts实例
  if (influenceChartInstance) {
    influenceChartInstance.dispose()
    influenceChartInstance = null
  }
  if (languageChartInstance) {
    languageChartInstance.dispose()
    languageChartInstance = null
  }
  if (sentimentChartInstance) {
    sentimentChartInstance.dispose()
    sentimentChartInstance = null
  }
  if (sourceTypeChartInstance) {
    sourceTypeChartInstance.dispose()
    sourceTypeChartInstance = null
  }
}

// 在组件卸载时清理资源
onUnmounted(() => {
  cleanup()

  // 清理观察器和监听器
  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }

  if (browserNavigationTimer) {
    clearTimeout(browserNavigationTimer)
  }

  document.removeEventListener('visibilitychange', handleVisibilityChange)
  window.removeEventListener('popstate', handleBrowserNavigation)
})
</script>

<!-- 全局穿透样式：只作用于数据统计页面，不影响其他页面 -->
<style>
/* 只在数据统计页面路由时应用这些样式，使用 :has() 选择器 */
body:has(.dashboard-container) {
  overflow: hidden !important; /* 避免全局滚动影响布局 */
}

/* 只在数据统计页面时重置 #app 的背景和滚动 */
#app:has(.dashboard-container) {
  overflow: hidden !important; /* 避免全局滚动影响布局 */
  background:
    url('/src/assets/data_imgs/星星背景.png'),
    radial-gradient(
      100% 177.78% at 100% 0%,
      rgba(25, 50, 90, 1) 0%,
      rgba(65, 40, 100, 1) 69.39%,
      rgba(25, 50, 90, 1) 100%
    ) !important;
  background-size:
    100% 100%,
    100% 100% !important;
  background-repeat: no-repeat, no-repeat !important;
  background-position: center, center !important;
  opacity: 1;
}
</style>

<!-- 组件内样式 -->
<style scoped>
/* 基础样式 - 全屏无空白 */
.dashboard-container {
  width: 100vw !important;
  min-height: 100vh !important;
  background:
    url('/src/assets/data_imgs/星星背景.png'),
    radial-gradient(
      100% 177.78% at 100% 0%,
      rgba(25, 50, 90, 1) 0%,
      rgba(65, 40, 100, 1) 69.39%,
      rgba(25, 50, 90, 1) 100%
    );
  background-size:
    100% 100%,
    100% 100%;
  background-repeat: no-repeat, no-repeat;
  background-position: center, center;
  background-attachment: fixed;
  opacity: 0.85;
  color: #00e1ff;
  font-family: 'Microsoft Yahei', sans-serif;
  padding: 6px !important;
  box-sizing: border-box;
  overflow-x: auto;
  overflow-y: auto;
  position: relative;
  top: 0 !important;
  left: 0 !important;
}

/* 重置数据统计页面内部元素的 box-sizing，但不影响外部页面 */
.dashboard-container * {
  box-sizing: border-box;
}

/* 头部样式 */
.dashboard-header {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  border-bottom: none;
  padding: 20px 40px !important;
  margin-bottom: 20px !important;
  background-image: url('/src/assets/data_imgs/标题框框.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-position: center 15px;
  min-height: 80px;
  box-sizing: border-box;
  z-index: 20; /* 确保标题栏在顶层 */
  filter: brightness(1.1); /* 增加亮度 */
}

.dashboard-header h1 {
  font-size: 40px;
  height: 52px;
  color: rgba(255, 255, 255, 1);
  margin: 0 !important;
  text-shadow:
    0 0 4px rgba(255, 255, 255, 0.3),
    0 0 6px #00e1ff;
  text-align: center;
  line-height: 52px;
  filter: brightness(1.2); /* 增加亮度 */
}

.header-right {
  position: absolute;
  right: 40px;
  top: 80%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 2px;
  align-items: flex-end;
}

.header-time {
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
}

/* 模式选择器 */
.mode-selector {
  position: relative;
  cursor: pointer;
}

.mode-text {
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
}

.mode-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  background: rgba(20, 55, 85, 0.95);
  border: 1px solid rgba(0, 225, 255, 0.6);
  border-radius: 4px;
  padding: 4px 0;
  min-width: 120px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.mode-option {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
  cursor: pointer;
  transition: background-color 0.2s;
}

.mode-option:hover {
  background: rgba(0, 225, 255, 0.3);
}

.mode-option.active {
  background: rgba(0, 225, 255, 0.4);
  color: rgba(0, 225, 255, 1);
}

/* 顶部卡片 */
.top-cards {
  display: flex;
  gap: 33px; /* 四个框框的间隔改为33px */
  margin-bottom: 16px !important;
  width: 100%;
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
  flex-wrap: wrap;
  margin-left: 0; /* 移除左边距计算，使用 justify-content: center 实现居中 */
}

.card-item {
  position: relative;
  display: flex;
  left: 0px;
  top: 0px;
  width: 425px;
  height: 140px;
  opacity: 1;
  background: linear-gradient(180deg, rgba(24, 65, 196, 0.2) 0%, rgba(20, 10, 125, 0.07) 100%);
  overflow: hidden;
  border: 0.6px solid rgba(40, 186, 243, 1);

  box-shadow: inset 0px 1px 10px rgba(110, 161, 255, 0.5);

  /* 垂直方向上居中 */
  align-items: center;
  /* 水平方向上居中 */
  justify-content: start;

  /* 让元素按垂直方向排列 */
  flex-direction: row;
  /* 可选：给卡片加内边距，让内容不贴边 */
  padding: 16px;
  box-sizing: border-box;
}
/* 角的基础样式 - 同时应用于card-item和panel */
.card-item .corner,
.panel .corner {
  position: absolute;
  width: 14px; /* 小方块的大小，和你图里一致 */
  height: 14px;
  border: 1px solid rgba(24, 219, 253, 1); /* 高亮颜色 */
  z-index: 10; /* 确保角在内容之上 */
}

/* 左上角：只显示上边框和左边框 */
.corner.top-left {
  top: 0;
  left: 0;
  border-right: none;
  border-bottom: none;
}

/* 右上角：只显示上边框和右边框 */
.corner.top-right {
  top: 0;
  right: 0;
  border-left: none;
  border-bottom: none;
}

/* 左下角：只显示下边框和左边框 */
.corner.bottom-left {
  bottom: 0;
  left: 0;
  border-right: none;
  border-top: none;
}

/* 右下角：只显示下边框和右边框 */
.corner.bottom-right {
  bottom: 0;
  right: 0;
  border-left: none;
  border-top: none;
}

.card-icon {
  position: relative;
  width: auto; /* 改为auto，保持原比例 */
  height: 50px; /* 固定高度，宽度自适应 */
  left: 40px;
  /* 确保图标背景透明，避免深色背景被遮挡 */
  background-color: transparent;
  /* 添加光晕效果，让图标在深色背景下更突出 */
  filter: drop-shadow(0 0 4px #00e1ff);
  /* 强制图标显示，避免被隐藏 */
  opacity: 1 !important;
  display: block !important;
  object-fit: contain; /* 保持原比例 */
}

.card-content {
  display: flex;
  position: relative;
  left: 50px;
  /* flex-direction: column; */
}

.card-number {
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 4px !important;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
}

.card-label {
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
  opacity: 0.8;
  position: relative;
  top: 13px;
  left: 5px;
}

/* 内容区域 - 三列flex布局，与顶部卡片对齐 */
.content-wrapper {
  display: flex;
  flex-direction: row;
  gap: 33px; /* 与顶部卡片间隔一致，改为33px */
  height: calc(100vh - 280px); /* 精确计算，确保不超出视角 */
  width: 100%;
  overflow: hidden; /* 防止超出视角 */
  justify-content: center; /* 水平居中对齐 */
  align-items: flex-start; /* 顶部对齐 */
  max-width: 100%;
  box-sizing: border-box;
  flex-wrap: wrap;
  margin-left: 0; /* 移除左边距计算，使用 justify-content: center 实现居中 */
}

.content-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 0;
}

/* 左列：与新闻数对齐，宽度380px（与卡片宽度一致） */
.content-column:first-child {
  width: 420px;
  flex-shrink: 0;
}

/* 中列：与站点数和语种数对齐，宽度为两个卡片宽度+一个gap = 380*2+16 = 776px */
.content-column:nth-child(2) {
  width: 883px;
  flex-shrink: 0;
}

/* 右列：与国家数对齐，宽度380px（与卡片宽度一致） */
.content-column:last-child {
  width: 420px;
  flex-shrink: 0;
}

.content-column:first-child .panel,
.content-column:nth-child(2) .panel {
  height: 344px; /* 减小高度以适应视角 */
  flex-shrink: 0;
}

/* 右列面板跨越两行，高度减小以适应视角 */
.content-column:last-child .panel {
  height: 725px; /* 300px * 2 + 16px gap = 616px */
  flex-shrink: 0;
}

.panel {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0; /* 防止flex子元素溢出 */
  overflow: hidden; /* 确保内容不溢出 */
  z-index: 10; /* 确保面板在顶层 */
  filter: brightness(1.1); /* 增加亮度 */
  width: 100%;
  box-sizing: border-box;
  opacity: 1;
  background: linear-gradient(180deg, rgba(24, 65, 196, 0.4) 0%, rgba(20, 10, 125, 0.18) 100%);
  border: 0.6px solid rgba(40, 186, 243, 1);
  box-shadow: inset 0px 1px 10px rgba(110, 161, 255, 0.7);
  padding: 12px !important;
  z-index: 10; /* 确保在顶层 */
  filter: brightness(1.1); /* 增加亮度 */
}

/* 使用背景图片的面板 - 小框 */
.panel-with-bg-image {
  background-image: url('/src/assets/data_imgs/可视化小框.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-position: center;
  background-color: transparent;
  border: none;
  box-shadow: none;
  padding: 20px 16px 16px 16px !important; /* 增加顶部padding以适应顶部边框设计 */
  z-index: 10; /* 确保在顶层 */
  filter: brightness(1.15); /* 增加亮度 */
}

/* 使用背景图片的面板 - 中框 */
.panel-with-middle-bg {
  background-image: url('/src/assets/data_imgs/可视化中框.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-position: center;
  background-color: transparent;
  border: none;
  box-shadow: none;
  padding: 20px 16px 16px 16px !important; /* 增加顶部padding以适应顶部边框设计 */
  z-index: 10; /* 确保在顶层 */
  filter: brightness(1.15); /* 增加亮度 */
}

/* 使用背景图片的面板 - 长框 */
.panel-with-long-bg {
  background-image: url('/src/assets/data_imgs/可视化长框.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-position: center;
  background-color: transparent;
  border: none;
  box-shadow: none;
  padding: 20px 16px 16px 16px !important; /* 增加顶部padding以适应顶部边框设计 */
  z-index: 10; /* 确保在顶层 */
  filter: brightness(1.15); /* 增加亮度 */
}

/* 信源分析面板 - 垂直分割成两个子面板 */
.source-analysis-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.source-analysis-panel > h3 {
  margin: 0 0 8px 0 !important;
  font-size: 16px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
  padding-bottom: 4px !important;
  border-bottom: 1px solid rgba(0, 225, 255, 0.4);
  flex-shrink: 0;
}

.sub-panel {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0; /* 防止flex子元素溢出 */
  overflow: hidden;
  /* 去掉框框：移除背景和边框 */
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 12px !important;
}

.panel h3 {
  margin: 0 0 8px 0 !important;
  font-size: 16px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
  padding-bottom: 4px !important;
  border-bottom: 1px solid rgba(0, 225, 255, 0.4);
  flex-shrink: 0;
}

/* 标题带装饰的容器 */
.title-with-decoration {
  position: relative;
  margin-bottom: 12px !important;
}

.title-with-decoration h3 {
  border-bottom: none;
  padding-bottom: 0 !important;
  margin-bottom: 0 !important;
}

/* 标题下方的装饰矩形 */
.title-decoration {
  position: relative;
  top: 5px;
  display: block;
  width: auto;
  height: auto;
  max-width: 100%;
  margin-top: 4px;
  margin-bottom: 0;
}

.panel h4 {
  margin: 0 0 8px 0 !important;
  font-size: 16px; /* 字体大小16px */
  font-weight: 400;
  line-height: 22px;
  color: rgba(22, 245, 255, 1); /* 指定颜色 */
  font-family: 'Microsoft Yahei', sans-serif;
  padding-bottom: 4px !important;
  border-bottom: 1px solid rgba(0, 225, 255, 0.4);
  flex-shrink: 0;
}

/* 信源类型分布标题 - 移除横线 */
.panel h4.no-border-bottom {
  border-bottom: none;
}

/* 标签页样式 */
.tabs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px !important;
}

.tabs {
  display: flex;
  gap: 0; /* 移除间隔，让选项卡连在一起 */
  flex-wrap: wrap;
  border-radius: 4px; /* 整体容器有圆角 */
  overflow: hidden; /* 隐藏内部元素的圆角，只显示外部的 */
}

/* 选项卡和图例在同一行 */
.tabs-with-legend {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px !important;
}

.tabs-with-legend .tabs {
  flex: 1;
  margin-bottom: 0 !important;
}

/* 情感分析图例 */
.sentiment-legend {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-shrink: 0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(0, 225, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
}

.legend-color {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.hotness-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
}

.hotness-icon {
  width: 16px;
  height: 16px;
}

.tab {
  padding: 4px 12px !important;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
  cursor: pointer;
  border-radius: 0; /* 移除圆角，让选项卡连在一起 */
  /* 无论是否选中都有框 */
  border: 1px solid rgba(0, 225, 255, 0.3);
  border-right: none; /* 移除右边框，让选项卡连在一起 */
  background: rgba(0, 20, 40, 0.3);
  transition: all 0.3s;
  position: relative;
  /* 使用负边距消除边框重叠 */
  margin-left: -1px;
}

/* 第一个选项卡左边有圆角，恢复左边距 */
.tab:first-child {
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
  margin-left: 0;
}

/* 最后一个选项卡右边有圆角和右边框 */
.tab:last-child {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  border-right: 1px solid rgba(0, 225, 255, 0.3);
}

.tab.active {
  /* 选中状态：尝试使用背景图片，如果无法紧贴则使用渐变样式 */
  /* 由于有padding，背景图片可能无法完全紧贴边框，使用渐变样式作为备选 */
  background: linear-gradient(90deg, rgba(0, 225, 255, 0.4) 0%, rgba(0, 180, 255, 0.3) 100%);
  /* 如果背景图片可以紧贴，取消上面的渐变，使用下面的背景图片 */
  /* background-image: url('/src/assets/data_imgs/选项卡.png'); */
  /* background-size: 100% 100%; */
  /* background-repeat: no-repeat; */
  /* background-position: center; */
  color: rgba(255, 255, 255, 1);
  padding: 4px 12px !important;
  border-color: rgba(0, 225, 255, 0.5);
  /* 选中时添加光晕效果 */
  box-shadow: inset 0 0 8px rgba(0, 225, 255, 0.3);
}

/* 选中状态的第一个选项卡左边有圆角 */
.tab.active:first-child {
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}

/* 选中状态的最后一个选项卡右边有圆角 */
.tab.active:last-child {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
}

/* 新闻列表 */
.news-list {
  list-style: none;
  padding: 0 !important;
  margin: 0 !important;
  flex: 1;
  overflow-y: auto;
}

.news-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0 !important;
  border-bottom: 1px solid rgba(0, 225, 255, 0.2);
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
  cursor: pointer; /* 鼠标悬停时显示小手 */
}

/* 排名图标 */
.rank-icon-img {
  width: auto;
  height: 20px;
  display: inline-block;
  vertical-align: middle;
  margin-right: 8px !important;
  flex-shrink: 0;
}

.news-title {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 8px !important;
}

/* 趋势箭头图标 */
.trend-icon {
  width: auto;
  height: 14px;
  display: inline-block;
  vertical-align: middle;
  margin-left: 4px;
}

.news-hot {
  color: rgba(255, 255, 255, 1); /* 改为白色 */
  display: flex;
  align-items: center;
}

/* 媒体列表 - 列表形式 */
.media-list {
  width: 100%;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.media-list-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 0; /* 去掉圆角 */
  background: transparent;
  font-size: 14px;
  font-weight: 400;
  line-height: 34px; /* 行高设为34px */
  height: 34px; /* 高度也设为34px */
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
  cursor: pointer; /* 鼠标悬停时显示小手 */
}

/* 奇数行更亮的背景（索引从0开始，所以0,2,4...是奇数行） */
.media-list-item:nth-child(odd) {
  background: rgba(0, 225, 255, 0.1); /* 奇数行更亮的背景 */
}

.media-rank {
  width: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.media-name {
  flex: 1;
  margin-left: 12px;
}

.media-score {
  width: 80px;
  text-align: right;
  flex-shrink: 0;
}

/* 排名图标样式 */
.rank-icon {
  width: auto;
  height: 20px;
  display: inline-block;
  vertical-align: middle;
}

/* 综合指数颜色：第一红色，第二橙色，第三黄色 */
.media-score.score-first {
  color: #ff0000; /* 红色 */
  font-weight: bold;
}

.media-score.score-second {
  color: #ffa500; /* 橙色 */
  font-weight: bold;
}

.media-score.score-third {
  color: #ffff00; /* 黄色 */
  font-weight: bold;
}

/* 图表容器 - 强制占满面板剩余空间 */
.chart-container {
  flex: 1;
  width: 100%;
  min-height: 0; /* 允许flex收缩 */
  overflow: hidden;
}

/* 指数汇总 */
.index-summary {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  color: rgba(255, 255, 255, 1);
  font-family: 'Microsoft Yahei', sans-serif;
  margin-bottom: 8px !important;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 34, 68, 0.5);
}

::-webkit-scrollbar-thumb {
  background: #00e1ff;
  border-radius: 2px;
}
</style>

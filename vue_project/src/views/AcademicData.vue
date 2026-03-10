<template>
  <div class="academic-data-page">
    <!-- 左侧导航栏 -->
    <div class="left-sidebar">
      <div class="nav-header">导航</div>
      <ul class="nav-list">
        <li
          class="nav-item"
          :class="{ active: activeNav === 'academic' }"
          @click="setActiveNav('academic')"
        >
          <span class="nav-icon">📚</span>
          <span class="nav-text">学术检索</span>
          <span class="nav-arrow">></span>
        </li>
        <li
          class="nav-item"
          :class="{ active: activeNav === 'politics' }"
          @click="setActiveNav('politics')"
        >
          <span class="nav-icon">🏛️</span>
          <span class="nav-text">政治与国际关系</span>
          <span class="nav-arrow">></span>
        </li>
        <li
          class="nav-item"
          :class="{ active: activeNav === 'military' }"
          @click="setActiveNav('military')"
        >
          <span class="nav-icon">⚔️</span>
          <span class="nav-text">军事</span>
          <span class="nav-arrow">></span>
        </li>
        <li
          class="nav-item"
          :class="{ active: activeNav === 'history' }"
          @click="setActiveNav('history')"
        >
          <span class="nav-icon">📜</span>
          <span class="nav-text">历史</span>
          <span class="nav-arrow">></span>
        </li>
        <li
          class="nav-item"
          :class="{ active: activeNav === 'economy' }"
          @click="setActiveNav('economy')"
        >
          <span class="nav-icon">💰</span>
          <span class="nav-text">经济</span>
          <span class="nav-arrow">></span>
        </li>
        <li class="nav-item" :class="{ active: activeNav === 'law' }" @click="setActiveNav('law')">
          <span class="nav-icon">⚖️</span>
          <span class="nav-text">法律</span>
          <span class="nav-arrow">></span>
        </li>
        <li
          class="nav-item"
          :class="{ active: activeNav === 'psychology' }"
          @click="setActiveNav('psychology')"
        >
          <span class="nav-icon">🧠</span>
          <span class="nav-text">心理</span>
          <span class="nav-arrow">></span>
        </li>
        <li
          class="nav-item"
          :class="{ active: activeNav === 'government' }"
          @click="setActiveNav('government')"
        >
          <span class="nav-icon">🏛️</span>
          <span class="nav-text">政府官方</span>
          <span class="nav-arrow">></span>
        </li>
        <li
          class="nav-item"
          :class="{ active: activeNav === 'international' }"
          @click="setActiveNav('international')"
        >
          <span class="nav-icon">🌍</span>
          <span class="nav-text">国际组织</span>
          <span class="nav-arrow">></span>
        </li>
      </ul>
    </div>

    <!-- 右侧主内容区 -->
    <div class="main-content">
      <!-- 搜索栏 -->
      <div class="search-section">
        <div class="search-input-group">
          <span class="search-icon">🔍</span>
          <input type="text" placeholder="请输入要查找的内容" class="search-input" />
        </div>
      </div>

      <!-- 分类标签 -->
      <div class="category-tabs">
        <div
          class="tab"
          :class="{ active: activeTab === 'academic' }"
          @click="setActiveTab('academic')"
        >
          学术检索
        </div>
        <div
          class="tab"
          :class="{ active: activeTab === 'politics' }"
          @click="setActiveTab('politics')"
        >
          政治与国际关系
        </div>
        <div
          class="tab"
          :class="{ active: activeTab === 'military' }"
          @click="setActiveTab('military')"
        >
          军事
        </div>
        <div
          class="tab"
          :class="{ active: activeTab === 'history' }"
          @click="setActiveTab('history')"
        >
          历史
        </div>
        <div
          class="tab"
          :class="{ active: activeTab === 'economy' }"
          @click="setActiveTab('economy')"
        >
          经济
        </div>
        <div class="tab" :class="{ active: activeTab === 'law' }" @click="setActiveTab('law')">
          法律
        </div>
        <div
          class="tab"
          :class="{ active: activeTab === 'psychology' }"
          @click="setActiveTab('psychology')"
        >
          心理
        </div>
        <div
          class="tab"
          :class="{ active: activeTab === 'government' }"
          @click="setActiveTab('government')"
        >
          政府官方
        </div>
        <div
          class="tab"
          :class="{ active: activeTab === 'international' }"
          @click="setActiveTab('international')"
        >
          国际组织
        </div>
      </div>
      <!-- 研究机构列表 -->
      <div class="institute-list">
        <div class="institute-item" v-for="institute in currentInstitutes" :key="institute.id">
          <div class="institute-logo">
            <div class="logo-circle" :style="{ backgroundColor: institute.logoColor }">
              {{ institute.logoText }}
            </div>
          </div>
          <div class="institute-content">
            <h3 class="institute-title">{{ institute.title }}</h3>
            <p class="institute-description">{{ institute.description }}</p>
            <div class="institute-meta">
              <span class="meta-item">
                <span class="meta-icon">🕒</span>
                {{ institute.updateTime }}
              </span>
              <span class="meta-item">
                <span class="meta-icon">✏️</span>
                {{ institute.author }}
              </span>
            </div>
            <div class="institute-actions">
              <span class="pdf-info">
                <span class="pdf-icon">📄</span>
                {{ institute.pages }}页
              </span>
              <button class="view-guide-btn">查看指南</button>
            </div>
          </div>
        </div>
      </div>
      <!-- 分页组件 -->
      <div class="pagination">
        <div class="pagination-info">
          <span>共 {{ totalItems }} 条</span>
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
import { ref, computed } from 'vue'

// 当前激活的导航项
const activeNav = ref('politics')
const activeTab = ref('politics')

// 设置激活的导航项
const setActiveNav = (nav) => {
  activeNav.value = nav
  activeTab.value = nav
}

// 设置激活的标签
const setActiveTab = (tab) => {
  activeTab.value = tab
  activeNav.value = tab
}

// 研究机构数据
const institutes = ref([
  {
    id: 1,
    title: 'Institute of Development Studies (发展研究所(IDS))',
    description:
      '发展研究所(IDS) 提供世界一流的研究、学习和教学,改变全球更公平和可持续发展所需的知识、行动和领导力。',
    updateTime: '2024-05-04 17:13:35',
    author: 'Peter Taylor',
    pages: '12',
    logoColor: '#dc3545',
    logoText: 'IDS',
  },
  {
    id: 2,
    title: 'Belfer Center for Science and International Affairs',
    description:
      '贝尔弗中心是约翰·肯尼迪政府学院在国际安全事务、环境和资源问题以及科技政策方面的研究、教学和培训中心。',
    updateTime: '2024-04-06 16:06:57',
    author: 'Harvard University',
    pages: '12',
    logoColor: '#6c757d',
    logoText: 'H',
  },
  {
    id: 3,
    title: 'Hudson Institute (哈德逊研究所)',
    description: '哈德逊研究所(Hudson Institute) 是美国一所非牟利智库,亦是全美五大保守派智库之一。',
    updateTime: '2024-04-04 23:49:42',
    author: 'Herman Kahn',
    pages: '12',
    logoColor: '#28a745',
    logoText: 'H',
  },
  {
    id: 4,
    title: '美国企业公共政策研究所(AEI)',
    description:
      '研究政府、政治、经济和社会福利,宣称的宗旨是:守护并改善美国自由和民主资本主义的原则与制度...',
    updateTime: '2024-03-24 11:28:26',
    author: 'Lewis H. Brown',
    pages: '12',
    logoColor: '#007bff',
    logoText: 'AEI',
  },
  {
    id: 5,
    title: 'The Heritage Foundation (传统基金会)',
    description:
      'Heritage 的使命是制定和推广基于自由企业、有限政府、个人自由、美国传统价值观和强大国防原则的公共政策。',
    updateTime: '2024-03-10 22:53:42',
    author: 'Joseph Cours and Paul Verrich',
    pages: '12',
    logoColor: '#6c757d',
    logoText: 'HF',
  },
  {
    id: 6,
    title: '美国进步中心 Center for American Progress (CAP)',
    description:
      '美国进步中心是一个独立的、无党派的政策研究所,致力于通过大胆、进步的思想、强有力的领导和协调一致的行动来改善所有美国人的生活。',
    updateTime: '2024-03-09 19:08:05',
    author: 'Patrick Gaspard',
    pages: '12',
    logoColor: '#007bff',
    logoText: 'CAP',
  },
  {
    id: 7,
    title: 'Peterson Institute for International Economics',
    description:
      '彼得森国际经济研究所 (Peterson Institute for International Economics) 是一个独立的、非营利性研究机构...',
    updateTime: '2024-03-08 16:30:00',
    author: 'Adam S. Posen',
    pages: '12',
    logoColor: '#007bff',
    logoText: 'PIIE',
  },
])

// 分页相关状态
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = ref(1420) // 根据实际数据量调整
const jumpPage = ref(1)

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(totalItems.value / pageSize.value)
})

// 计算当前页的数据
const currentInstitutes = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value
  const endIndex = startIndex + pageSize.value
  return institutes.value.slice(startIndex, endIndex)
})

// 计算可见的页码
const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})

// 跳转到指定页面
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    scrollToTop()
  }
}

// 跳转到指定页面（输入框）
const jumpToPage = () => {
  try {
    const page = parseInt(jumpPage.value)
    if (isNaN(page)) {
      jumpPage.value = currentPage.value
      return
    }
    if (page >= 1 && page <= totalPages.value) {
      goToPage(page)
    } else {
      jumpPage.value = currentPage.value
    }
  } catch (error) {
    console.error('跳转页面时发生错误:', error)
    jumpPage.value = currentPage.value
  }
}

// 改变每页显示数量
const handlePageSizeChange = () => {
  currentPage.value = 1
  scrollToTop()
}

// 滚动到顶部
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  })
}
</script>

<style scoped lang="css">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.academic-data-page {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* 左侧导航栏 - 核心修改区 */
.left-sidebar {
  width: 280px;
  background-color: #f8f9fa;
  border-right: 1px solid #e9ecef;
  /* 移除上下内边距，避免整体偏移 */
  padding: 0;
  position: fixed;
  top: 60px;
  left: 0;
  bottom: 0;
  overflow-y: auto;
}

.nav-header {
  /* 仅保留左右内边距，上下调整为16px保持美观 */
  padding: 16px 20px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  border-bottom: 1px solid #e9ecef;
  /* 移除底部外边距 */
  margin-bottom: 0;
}

.nav-list {
  display: flex;
  flex-direction: column;
  list-style: none;
  gap: 0;
  /* 清除列表默认内边距，确保完全靠左 */
  padding-left: 0;
  margin: 0;
}

.nav-item {
  height: 50px;
  display: flex;
  align-items: center;
  /* 调整内边距，仅保留左侧20px（视觉对齐），上下保留，左右清零 */
  padding: 0 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  /* 移除左侧边框，改为整行背景高亮 */
  border-left: none;
  /* 确保内容靠左 */
  justify-content: flex-start;
  /* 宽度100%，确保整行可点击 */
  width: 100%;
}

.nav-item:hover {
  background-color: #e9ecef;
}

/* 激活样式 - 核心修改：整行高亮 */
.nav-item.active {
  background-color: #dee2e6;
  /* 整行背景覆盖，移除原有小圆点 */
  position: relative;
  /* 左侧添加竖线标识，宽度100% */
  border-left: 3px solid #dc3545;
}

/* 移除原有小圆点，改为整行高亮+左侧竖线 */
.nav-item.active::before {
  display: none;
}

.nav-icon {
  font-size: 16px;
  margin-right: 12px;
  width: 20px;
  text-align: center;
}

.nav-text {
  flex: 1;
  font-size: 14px;
  color: #333;
}

.nav-arrow {
  font-size: 12px;
  color: #6c757d;
}

/* 右侧主内容区 */
.main-content {
  position: fixed;
  top: 60px;
  left: 280px;
  right: 0;
  bottom: 0;
  padding: 30px 40px;
  background-color: #fff;
  /* 允许内部内容滚动 */
  overflow-y: auto;
}

/* 搜索区域 */
.search-section {
  margin-bottom: 30px;
}

.search-input-group {
  position: relative;
  max-width: 1200px;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  color: #6c757d;
}

.search-input {
  width: 100%;
  padding: 12px 15px 12px 45px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
  background-color: #fff;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

/* 分类标签 */
.category-tabs {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.tab {
  padding: 8px 16px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #6c757d;
  transition: all 0.3s ease;
}

.tab:hover {
  background-color: #e9ecef;
  color: #333;
}

.tab.active {
  background-color: #667eea;
  color: #fff;
  border-color: #667eea;
}

/* 研究机构列表 */
.institute-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.institute-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.institute-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.institute-logo {
  flex-shrink: 0;
}

.logo-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: bold;
  font-size: 14px;
}

.institute-content {
  flex: 1;
}

.institute-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.4;
}

.institute-description {
  font-size: 14px;
  color: #6c757d;
  line-height: 1.5;
  margin-bottom: 12px;
}

.institute-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: #6c757d;
}

.meta-icon {
  font-size: 12px;
}

.institute-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.pdf-info {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: #dc3545;
}

.pdf-icon {
  font-size: 12px;
}

.view-guide-btn {
  padding: 6px 16px;
  background-color: #667eea;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-guide-btn:hover {
  background-color: #5a6fd8;
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .left-sidebar {
    width: 100%;
    position: relative;
    top: 0;
  }

  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 20px;
  }

  .category-tabs {
    gap: 10px;
  }

  .tab {
    padding: 6px 12px;
    font-size: 13px;
  }
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  padding: 20px 0;
  border-top: 1px solid #e9ecef;
  gap: 140px;
}

.pagination-info {
  display: flex;
  align-items: center;
  gap: 15px;
  color: #6c757d;
  font-size: 14px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 5px;
}

.page-btn {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  background-color: #fff;
  color: #333;
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

.pagination-jump {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6c757d;
  font-size: 14px;

  input {
    width: 60px;
    padding: 6px 8px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 14px;
    text-align: center;

    &:focus {
      outline: none;
      border-color: #667eea;
    }
  }
}
</style>

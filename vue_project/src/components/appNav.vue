<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowDown, Search, User, Document, Bell, TrendCharts, Aim, Folder, SwitchButton } from '@element-plus/icons-vue' // 补全缺失的图标导入，避免报错
import { getToken, getAuthChangedEventName } from '@/utils/auth'

const router = useRouter()
const route = useRoute()

// 监听路由变化，确保组件状态正确
const currentPath = ref(route.path)

const hasToken = ref(!!getToken())

// 添加监听路由变化的方法
const handleRouteChange = () => {
  currentPath.value = route.path
  hasToken.value = !!getToken()
  // 重置所有下拉菜单状态
  isDataServiceDropdownOpen.value = false
  isUserCenterDropdownOpen.value = false
  // 清除所有定时器
  if (dataServiceTimer) {
    clearTimeout(dataServiceTimer)
    dataServiceTimer = null
  }
  if (userCenterTimer) {
    clearTimeout(userCenterTimer)
    userCenterTimer = null
  }
}

// 新增：判断当前页面是否需要隐藏导航栏
const shouldHideNavbar = computed(() => {
  return route.meta?.hideNavbar === true
})

// 判断是否是首页
const isHomePage = computed(() => {
  return route.path === '/'
})

// 检查数据服务系统是否应该高亮
const isDataServiceActive = computed(() => {
  return route.path.startsWith('/data-') || route.path === '/data-service'
})

// 数据服务系统下拉菜单状态
const isDataServiceDropdownOpen = ref(false)
// 用户中心下拉菜单状态
const isUserCenterDropdownOpen = ref(false)

// 定时器引用
let dataServiceTimer = null
let userCenterTimer = null

// 监听自定义事件，当返回首页时重置状态
const handleRouteToHome = () => {
  isDataServiceDropdownOpen.value = false
  isUserCenterDropdownOpen.value = false

  if (dataServiceTimer) {
    clearTimeout(dataServiceTimer)
    dataServiceTimer = null
  }
  if (userCenterTimer) {
    clearTimeout(userCenterTimer)
    userCenterTimer = null
  }
}

onMounted(() => {
  // 监听路由变化
  router.afterEach(handleRouteChange)
  // 监听自定义事件
  window.addEventListener('routeToHome', handleRouteToHome)
  // 路由回退时，强制触发页面重绘，解决布局错乱
  window.dispatchEvent(new Event('resize'))
  window.addEventListener(getAuthChangedEventName(), handleRouteChange)

  // document.body.style.paddingTop = '60px'
})

onUnmounted(() => {
  // 移除监听器
  if (dataServiceTimer) {
    clearTimeout(dataServiceTimer)
  }
  if (userCenterTimer) {
    clearTimeout(userCenterTimer)
  }
  window.removeEventListener('routeToHome', handleRouteToHome)
  window.removeEventListener(getAuthChangedEventName(), handleRouteChange)

  if (shouldHideNavbar.value) {
    document.body.style.paddingTop = '0'
  }
})

// 鼠标进入数据服务系统导航项
const enterDataServiceDropdown = () => {
  isDataServiceDropdownOpen.value = true
  // 关闭用户中心下拉菜单
  isUserCenterDropdownOpen.value = false
  // 清除关闭定时器
  if (dataServiceTimer) {
    clearTimeout(dataServiceTimer)
    dataServiceTimer = null
  }
}

// 鼠标进入数据服务系统下拉菜单内容
const enterDataServiceDropdownContent = () => {
  // 清除关闭定时器
  if (dataServiceTimer) {
    clearTimeout(dataServiceTimer)
    dataServiceTimer = null
  }
}

// 鼠标离开数据服务系统下拉菜单
const leaveDataServiceDropdown = () => {
  // 延迟2秒关闭，给用户更多时间操作
  dataServiceTimer = setTimeout(() => {
    isDataServiceDropdownOpen.value = false
  }, 2000)
}

// 鼠标进入用户中心导航项
const enterUserCenterDropdown = () => {
  isUserCenterDropdownOpen.value = true
  // 关闭数据服务系统下拉菜单
  isDataServiceDropdownOpen.value = false
  // 清除关闭定时器
  if (userCenterTimer) {
    clearTimeout(userCenterTimer)
    userCenterTimer = null
  }
}

// 鼠标进入用户中心下拉菜单内容
const enterUserCenterDropdownContent = () => {
  // 清除关闭定时器
  if (userCenterTimer) {
    clearTimeout(userCenterTimer)
    userCenterTimer = null
  }
}

// 鼠标离开用户中心下拉菜单
const leaveUserCenterDropdown = () => {
  // 延迟2秒关闭，给用户更多时间操作
  userCenterTimer = setTimeout(() => {
    isUserCenterDropdownOpen.value = false
  }, 2000)
}

// 导航到指定路由
const navigateTo = (path) => {
  router.push(path)
  // 关闭所有下拉菜单
  isDataServiceDropdownOpen.value = false
  isUserCenterDropdownOpen.value = false
  // 清除所有定时器
  if (dataServiceTimer) {
    clearTimeout(dataServiceTimer)
    dataServiceTimer = null
  }
  if (userCenterTimer) {
    clearTimeout(userCenterTimer)
    userCenterTimer = null
  }
}
</script>

<template>
  <div class="header" :class="{ 'header-transparent': isHomePage, 'header-white': !isHomePage }" v-if="!shouldHideNavbar">
    <div class="middle">
      <div class="logo" @click="router.push('/')" title="返回首页">
        <div class="logo-icon">
          <div class="block-1"></div>
          <div class="block-2"></div>
        </div>
        <span class="logo-text">
          <span class="logo-tipping">TIPPING</span>
          <span class="logo-point">POINT</span>
        </span>
      </div>
      <ul class="nav-list">
        <!-- 使用 <router-link> 实现路由跳转，to 属性指定目标路径 -->
        <li class="nav-item"><router-link to="/">首页</router-link></li>
        <li class="nav-item"><router-link to="/sentiment-analysis">舆情分析系统</router-link></li>
        <li class="nav-item"><router-link to="/open-computing">开源计算平台</router-link></li>
        <li class="nav-item"><router-link to="/academic-data">学术数据导航</router-link></li>

        <li
          class="nav-item dropdown-item"
          :class="{ 'nav-item-active': isDataServiceActive }"
          @mouseenter="enterDataServiceDropdown"
          @mouseleave="leaveDataServiceDropdown"
        >
          <div class="dropdown-trigger" @click="navigateTo('/data-service/data-search')">
            <span>数据服务系统</span>
            <el-icon class="dropdown-icon" :class="{ rotate: isDataServiceDropdownOpen }">
              <ArrowDown />
            </el-icon>
          </div>
          <div
            class="dropdown-menu"
            :class="{ show: isDataServiceDropdownOpen }"
            @mouseenter="enterDataServiceDropdownContent"
            @mouseleave="leaveDataServiceDropdown"
          >
            <!-- 修改后 -->
            <div
              class="dropdown-item-content"
              @click="navigateTo('/data-service/data-search')"
              style="--item-index: 0"
            >
              <el-icon class="dropdown-item-icon"><Document /></el-icon>
              <span>数据搜素</span>
            </div>

            <!-- 其他子项也相应修改 -->
            <div
              class="dropdown-item-content"
              @click="navigateTo('/data-service/alert-center')"
              style="--item-index: 2"
            >
              <el-icon class="dropdown-item-icon"><Bell /></el-icon>
              <span>预警中心</span>
            </div>

            <div
              class="dropdown-item-content"
              @click="navigateTo('/data-service/report-center')"
              style="--item-index: 3"
            >
              <el-icon class="dropdown-item-icon"><Document /></el-icon>
              <span>报告中心</span>
            </div>

            <div
              class="dropdown-item-content"
              @click="navigateTo('/data-service/data-statistics')"
              style="--item-index: 4"
            >
              <el-icon class="dropdown-item-icon"><TrendCharts /></el-icon>
              <span>数据统计</span>
            </div>
          </div>
        </li>
        <li
          v-if="hasToken"
          class="nav-item dropdown-item"
          @mouseenter="enterUserCenterDropdown"
          @mouseleave="leaveUserCenterDropdown"
        >
          <div class="dropdown-trigger">
            <span>用户中心</span>
            <el-icon class="dropdown-icon" :class="{ rotate: isUserCenterDropdownOpen }">
              <ArrowDown />
            </el-icon>
          </div>
          <div
            class="dropdown-menu"
            :class="{ show: isUserCenterDropdownOpen }"
            @mouseenter="enterUserCenterDropdownContent"
            @mouseleave="leaveUserCenterDropdown"
          >
            <div
              class="dropdown-item-content"
              style="--item-index: 0"
              @click="navigateTo('/user-center/personal-center')"
            >
              <el-icon class="dropdown-item-icon"><User /></el-icon>
              <span>个人中心</span>
            </div>
            <div
              class="dropdown-item-content"
              @click="navigateTo('/user-center/my-applications')"
              style="--item-index: 1"
            >
              <el-icon class="dropdown-item-icon"><Aim /></el-icon>
              <span>我的应用</span>
            </div>
            <div
              class="dropdown-item-content"
              @click="navigateTo('/user-center/help-docs')"
              style="--item-index: 2"
            >
              <el-icon class="dropdown-item-icon"><Document /></el-icon>
              <span>帮助文档</span>
            </div>
            <div
              class="dropdown-item-content"
              @click="navigateTo('/user-center/my-collections')"
              style="--item-index: 3"
            >
              <el-icon class="dropdown-item-icon"><Folder /></el-icon>
              <span>我的收录</span>
            </div>
            <div
              class="dropdown-item-content"
              @click="navigateTo('/user-center/logout')"
              style="--item-index: 4"
            >
              <el-icon class="dropdown-item-icon"><SwitchButton /></el-icon>
              <span>退出登录</span>
            </div>
          </div>
        </li>
        <li class="nav-item about-us-btn"><router-link to="/about-us">关于我们</router-link></li>
        <li class="nav-item about-us-btn"><router-link to="/user-center/help-docs" class="nav-link-help">使用说明</router-link></li>
      </ul>

      <!-- 右侧功能图标 -->
      <div class="header-actions">
        <button class="action-btn search-btn" @click="navigateTo('/data-service/data-search')" title="数据搜索">
          <el-icon size="20"><Search /></el-icon>
        </button>
        <button class="action-btn user-btn" @click="navigateTo(hasToken ? '/user-center/personal-center' : '/login')" title="个人中心">
          <el-icon size="20"><User /></el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;

}

/* 1. 移除强行重置body padding-top的样式，避免和首页布局冲突 */
.dashboard-container {
  margin-top: 0 !important;
  width: 100vw;
  height: 100vh;
}

.header {
  padding: 16px 24px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  z-index: 20;
  will-change: transform;
  backface-visibility: hidden;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

/* 首页导航栏：透明背景 */
.header-transparent {
  background-color: transparent;
  box-shadow: none;
}

/* 其他页面导航栏：白色背景 */
.header-white {
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.middle {
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: space-between;
}

/* Logo样式 */
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-right: 80px;
  flex-shrink: 0;
  cursor: pointer; /* 合并logo的cursor样式，精简代码 */
}

.logo-icon {
  width: 32px;
  height: 32px;
  position: relative;
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
}

.logo-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 14px;
  height: 14px;
  background: #667eea;
  border-radius: 2px;
}

.logo-icon::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 14px;
  height: 14px;
  background: #667eea;
  border-radius: 2px;
}

.logo-icon .block-1 {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 14px;
  height: 14px;
  background: #667eea;
  border-radius: 2px;
}

.logo-icon .block-2 {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 14px;
  height: 14px;
  background: #667eea;
  border-radius: 2px;
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
}

.logo-tipping {
  color: #333;
}

.logo-point {
  color: #667eea;
}

/* 导航列表 */
.nav-list {
  display: flex;
  list-style: none;
  gap: 100px;
  align-items: center;
  /* 2. 移除绝对定位，改用flex布局居中，避免回退时重绘异常 */
  margin: 0 auto;
  white-space: nowrap;
  flex-shrink: 0;
}

.nav-item {
  position: relative;
  white-space: nowrap;
  flex-shrink: 0;
}

.nav-item a {
  text-decoration: none;
  color: #999;
  font-size: 16px;
  font-weight: 600;
  padding: 8px 0;
  transition: color 0.3s ease;
  white-space: nowrap;
  display: inline-block;
}

.nav-item a:hover {
  color: #333;
}

/* 激活状态样式 */
.nav-item .router-link-active {
  color: #333;
  font-weight: 600;
}

.nav-item .router-link-active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 3px;
  background: #667eea;
  border-radius: 2px;
}

/* 下拉菜单项的激活状态样式 */
.nav-item-active .dropdown-trigger span {
  color: #333;
  font-weight: 600;
}

.nav-item-active .dropdown-trigger::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 3px;
  background: #667eea;
  border-radius: 2px;
}

/* 关于我们按钮样式 */
.about-us-btn a {
  color: #667eea;
  border: 1px solid #667eea;
  padding: 8px 16px;
  border-radius: 6px;
  background: transparent;
  transition: all 0.3s ease;
  font-size: 16px;
  font-weight: 500;
}

.about-us-btn a:hover {
  background: #667eea;
  color: white;
}

/* 使用说明：与关于我们同字体，无边框，颜色与左侧导航标题一致为灰色 */
.nav-link-help {
  color: #999 !important;
  border: none !important;
  background: transparent !important;
}
.nav-link-help:hover {
  color: #333 !important;
  background: transparent !important;
}
.nav-link-help.router-link-active {
  color: #333 !important;
  background: transparent !important;
}

.about-us-btn .router-link-active {
  background: #667eea;
  color: white;
}

/* 移除"关于我们"激活状态下的下划线 */
.about-us-btn .router-link-active::after {
  display: none;
}

/* 下拉菜单样式 */
.dropdown-item {
  position: relative;
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  color: #999;
  font-size: 16px;
  font-weight: 400;
  padding: 8px 0;
  transition: color 0.3s ease;
  text-decoration: none;
}

.dropdown-trigger:hover {
  color: #333;
}

.dropdown-icon {
  font-size: 12px;
  transition: transform 0.3s ease;
}

.dropdown-icon.rotate {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 160px;
  padding: 8px 0;
  margin-top: 5px;
  /* 确保下拉菜单有足够的点击区域 */
  pointer-events: auto;
  /* 滚动动画效果 */
  transform-origin: top;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  /* 初始状态：向上滚动隐藏 */
  transform: translateY(-15px) scaleY(0.8);
  opacity: 0;
  visibility: hidden;
}

/* 下拉菜单显示状态 */
.dropdown-menu.show {
  transform: translateY(0) scaleY(1);
  opacity: 1;
  visibility: visible;
}

/* 下拉菜单项动画延迟 */
.dropdown-menu.show .dropdown-item-content {
  animation: slideInFromTop 0.3s ease-out forwards;
  animation-delay: calc(var(--item-index) * 0.05s);
  opacity: 0;
  transform: translateY(-10px);
}

@keyframes slideInFromTop {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item-content {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px; /* 增加内边距，提供更大的点击区域 */
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  color: #999;
  /* 确保点击区域足够大 */
  min-height: 20px;
  /* 防止文本选择 */
  user-select: none;
}

.dropdown-item-content:hover {
  background-color: #f8f9fa;
  color: #333;
}

.dropdown-item-icon {
  font-size: 16px;
  color: #667eea;
}

/* 右侧功能图标 */
.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: auto;
  flex-shrink: 0;
}

.action-btn {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  color: #666;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn .el-icon {
  color: inherit;
}

.action-btn:hover {
  background: #f5f5f5;
  color: #333;
}

.search-btn:hover {
  color: #667eea;
}

.user-btn:hover {
  color: #667eea;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .nav-list {
    gap: 90px;
  }

  .nav-item a {
    font-size: 15px;
  }

  .about-us-btn a {
    font-size: 17px;
  }
}

@media (max-width: 1024px) {
  .nav-list {
    gap: 80px;
  }

  .nav-item a {
    font-size: 14px;
  }

  .about-us-btn a {
    font-size: 16px;
  }

  .logo {
    margin-right: 40px;
  }
}

@media (max-width: 768px) {
  .nav-list {
    gap: 70px;
  }

  .nav-item a {
    font-size: 13px;
  }

  .about-us-btn a {
    font-size: 15px;
  }

  .logo {
    margin-right: 20px;
  }

  .logo-text {
    font-size: 16px;
  }
}
</style>

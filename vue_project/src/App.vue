<script setup>
import AppNav from './components/appNav.vue'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 在路由变化时滚动到顶部
onMounted(() => {
  router.afterEach((to, from) => {
    // 如果目标路由是数据统计页面，强制重置所有滚动位置
    if (to.path === '/data-service/data-statistics') {
      window.scrollTo({ top: 0, left: 0, behavior: 'instant' })
      document.documentElement.scrollTop = 0
      document.body.scrollTop = 0
      return
    }
    // 其他页面正常滚动到顶部
    window.scrollTo(0, 0)
  })
})
</script>

<template>
  <div id="app">
    <appNav />
    <router-view v-slot="{ Component }">
      <keep-alive :include="['appHome']">
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </div>
</template>

<style scoped>

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden;
}
#app {
  min-height: 100vh;
  width: 100vw;
  overflow-x: hidden;
}

.main-content {
  padding-top: 0px; /* 为固定导航栏预留空间 */
  min-height: calc(100vh - 60px);
}
</style>

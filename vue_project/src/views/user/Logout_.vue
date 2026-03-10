<template>
  <div class="logout-page">
    <div class="logout-card">
      <p class="message">已退出登录</p>
      <p class="hint">正在跳转到首页...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { clearAuth } from '@/utils/auth'
const router = useRouter()

onMounted(() => {
  clearAuth()
  const t = setTimeout(() => {
    router.replace('/')
  }, 800)
  return () => clearTimeout(t)
})
</script>

<style scoped>
.logout-page {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
}
.logout-card {
  background: #fff;
  padding: 2rem 3rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  text-align: center;
}
.message {
  font-size: 1.1rem;
  color: #333;
  margin: 0 0 0.5rem 0;
}
.hint {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}
</style>

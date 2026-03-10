<template>
  <div class="login-page">
    <div class="login-card">
      <h1>用户登录</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-item">
          <label>用户名</label>
          <input v-model="username" type="text" required placeholder="请输入用户名" />
        </div>
        <div class="form-item">
          <label>密码</label>
          <input v-model="password" type="password" required placeholder="请输入密码" />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
        <div class="links">
          <router-link to="/register">注册账号</router-link>
          <router-link to="/forgot-password">忘记密码</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { API_PREFIX } from '@/config/api'
import { getToken, setToken, setCurrentUser } from '@/utils/auth'

const router = useRouter()
const route = useRoute()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const res = await fetch(`${API_PREFIX}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value }),
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.detail || '登录失败'
      return
    }
    if (data.access_token) {
      setToken(data.access_token)
      if (data.user) {
        setCurrentUser(data.user)
      }
      const redirect = route.query.redirect || '/'
      router.replace(redirect)
    } else {
      error.value = '未返回 token'
    }
  } catch (e) {
    error.value = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (getToken()) {
    const redirect = route.query.redirect || '/'
    router.replace(redirect)
  }
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2f5;
}
.login-card {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 360px;
}
.login-card h1 {
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  text-align: center;
}
.login-form .form-item {
  margin-bottom: 1rem;
}
.login-form label {
  display: block;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}
.login-form input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-sizing: border-box;
}
.login-form .error {
  color: #f56c6c;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}
.login-form button {
  width: 100%;
  padding: 0.6rem;
  margin-top: 0.5rem;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.login-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.links {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}
.links a {
  color: #409eff;
  text-decoration: none;
}
</style>

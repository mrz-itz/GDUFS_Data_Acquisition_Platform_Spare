<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1>用户注册</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-item">
          <label>用户名</label>
          <input v-model.trim="form.username" required placeholder="请输入用户名" />
        </div>
        <div class="form-item">
          <label>姓名</label>
          <input v-model.trim="form.full_name" required placeholder="请输入姓名" />
        </div>
        <div class="form-item">
          <label>邮箱</label>
          <input v-model.trim="form.email" type="email" required placeholder="请输入邮箱" />
        </div>
        <div class="form-item">
          <label>手机号</label>
          <input v-model.trim="form.phone" required placeholder="请输入手机号" />
        </div>
        <div class="form-item">
          <label>密码</label>
          <input v-model="form.password" type="password" required placeholder="请输入密码" />
        </div>
        <div class="form-item">
          <label>确认密码</label>
          <input v-model="form.confirm_password" type="password" required placeholder="请再次输入密码" />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="success" class="success">{{ success }}</p>
        <button type="submit" :disabled="loading">{{ loading ? '提交中...' : '注册' }}</button>
      </form>
      <p class="tips">已有账号？<router-link to="/login">去登录</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { API_PREFIX } from '@/config/api'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const success = ref('')
const form = reactive({
  username: '',
  full_name: '',
  email: '',
  phone: '',
  password: '',
  confirm_password: '',
})

async function handleRegister() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    const res = await fetch(`${API_PREFIX}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.detail || '注册失败'
      return
    }
    success.value = '注册成功，正在跳转登录页...'
    setTimeout(() => router.replace('/login'), 900)
  } catch (e) {
    error.value = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f0f2f5; }
.auth-card { background: #fff; padding: 24px; width: 420px; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,.1); }
.form-item { margin-bottom: 12px; }
.form-item label { display: block; margin-bottom: 4px; font-size: 13px; color: #555; }
.form-item input { width: 100%; padding: 8px 10px; border: 1px solid #dcdfe6; border-radius: 4px; }
button { width: 100%; margin-top: 6px; border: 0; background: #409eff; color: #fff; padding: 10px 0; border-radius: 4px; cursor: pointer; }
button:disabled { opacity: .6; cursor: not-allowed; }
.error { color: #f56c6c; font-size: 13px; }
.success { color: #67c23a; font-size: 13px; }
.tips { margin: 12px 0 0; font-size: 13px; text-align: center; }
</style>

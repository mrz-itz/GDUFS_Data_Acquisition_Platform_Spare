<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { API_PREFIX } from '@/config/api'
import { clearAuth, getToken, setCurrentUser } from '@/utils/auth'

const router = useRouter()
const loading = ref(false)
const savingProfile = ref(false)
const changingPwd = ref(false)
const activeTab = ref('basic-info')
const formData = reactive({ full_name: '', email: '', phone: '' })
const profile = reactive({ username: '', full_name: '', email: '', phone: '', created_at: '' })
const passwordForm = reactive({ old_password: '', new_password: '', confirm_password: '' })

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${getToken()}`,
  }
}

async function loadProfile() {
  loading.value = true
  try {
    const res = await fetch(`${API_PREFIX}/user/profile`, { headers: authHeaders() })
    const data = await res.json()
    if (!res.ok) {
      throw new Error(data.detail || '获取个人资料失败')
    }
    profile.username = data.username || ''
    profile.full_name = data.full_name || ''
    profile.email = data.email || ''
    profile.phone = data.phone || ''
    profile.created_at = data.created_at ? data.created_at.replace('T', ' ').slice(0, 19) : ''
    formData.full_name = profile.full_name
    formData.email = profile.email
    formData.phone = profile.phone
    setCurrentUser(data)
  } catch (e) {
    ElMessage.error(e.message || '获取个人资料失败')
    if ((e.message || '').includes('未登录')) {
      clearAuth()
      router.replace('/login')
    }
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  savingProfile.value = true
  try {
    const res = await fetch(`${API_PREFIX}/user/profile`, {
      method: 'PUT',
      headers: authHeaders(),
      body: JSON.stringify(formData),
    })
    const data = await res.json()
    if (!res.ok) {
      throw new Error(data.detail || '保存失败')
    }
    ElMessage.success('资料更新成功')
    await loadProfile()
  } catch (e) {
    ElMessage.error(e.message || '保存失败')
  } finally {
    savingProfile.value = false
  }
}

async function handlePasswordSubmit() {
  changingPwd.value = true
  try {
    const res = await fetch(`${API_PREFIX}/user/change-password`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(passwordForm),
    })
    const data = await res.json()
    if (!res.ok) {
      throw new Error(data.detail || '修改密码失败')
    }
    ElMessage.success('密码修改成功')
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (e) {
    ElMessage.error(e.message || '修改密码失败')
  } finally {
    changingPwd.value = false
  }
}

onMounted(loadProfile)
</script>

<template>
  <div class="personal-center-container">
    <div class="user-info-panel">
      <div class="user-header">
        <h3>个人信息</h3>
      </div>
      <div class="user-details">
        <div class="detail-item"><span class="label">用户名</span><span class="value">{{ profile.username || '--' }}</span></div>
        <div class="detail-item"><span class="label">姓名</span><span class="value">{{ profile.full_name || '--' }}</span></div>
        <div class="detail-item"><span class="label">手机号</span><span class="value">{{ profile.phone || '--' }}</span></div>
        <div class="detail-item"><span class="label">邮箱</span><span class="value">{{ profile.email || '--' }}</span></div>
        <div class="detail-item"><span class="label">创建时间</span><span class="value">{{ profile.created_at || '--' }}</span></div>
      </div>
    </div>

    <div class="basic-info-panel">
      <div class="tabs">
        <span class="tab" :class="{ active: activeTab === 'basic-info' }" @click="activeTab = 'basic-info'">基本资料</span>
        <span class="tab" :class="{ active: activeTab === 'password' }" @click="activeTab = 'password'">修改密码</span>
      </div>

      <div class="form-container" v-loading="loading">
        <el-form v-if="activeTab === 'basic-info'" :model="formData" label-width="80px">
          <el-form-item label="姓名"><el-input v-model="formData.full_name" placeholder="请输入姓名" /></el-form-item>
          <el-form-item label="邮箱"><el-input v-model="formData.email" placeholder="请输入邮箱" /></el-form-item>
          <el-form-item label="手机号"><el-input v-model="formData.phone" placeholder="请输入手机号" /></el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="savingProfile" @click="handleSave">保存</el-button>
          </el-form-item>
        </el-form>

        <el-form v-else :model="passwordForm" label-width="100px">
          <el-form-item label="当前密码"><el-input v-model="passwordForm.old_password" type="password" show-password /></el-form-item>
          <el-form-item label="新密码"><el-input v-model="passwordForm.new_password" type="password" show-password /></el-form-item>
          <el-form-item label="确认新密码"><el-input v-model="passwordForm.confirm_password" type="password" show-password /></el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="changingPwd" @click="handlePasswordSubmit">修改密码</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.personal-center-container {
  position: relative;
  top: 65px;
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.user-info-panel {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  max-width: 320px;
}

.user-header { margin-bottom: 20px; }

.user-details {
  font-size: 14px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}
.detail-item:last-child { border-bottom: none; }

.label {
  color: #666;
  display: flex;
  align-items: center;
  gap: 5px;
}

.value {
  color: #333;
}

.basic-info-panel {
  flex: 2;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.panel-header {
  margin-bottom: 20px;
}

.tabs {
  display: flex;
  gap: 20px;
  border-bottom: 1px solid #e9ecef;
}

.tab {
  padding: 10px 0;
  cursor: pointer;
  transition: all 0.3s ease;
}
.tab.active { color: #409eff; border-bottom: 2px solid #409eff; font-weight: bold; }

.form-container {
  padding: 20px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-form-item__label {
  font-weight: normal;
  color: #333;
}

.el-input {
  width: 100%;
}

.el-radio-group {
  display: flex;
  gap: 10px;
}

.el-radio {
  margin-right: 10px;
}

.el-button {
  margin-right: 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .personal-center-container {
    flex-direction: column;
  }

  .user-info-panel {
    max-width: 100%;
  }

  .basic-info-panel {
    max-width: 100%;
  }
}
</style>

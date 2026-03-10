<template>
  <div class="warning-management-page">
    <!-- 左侧预警分类栏 -->
    <div class="left-sidebar">
      <el-button
        type="primary"
        @click="showAddWarningDialog = true"
        class="add-warning-btn"
      >
        <el-icon><Plus /></el-icon> 新增预警
      </el-button>
      <el-input
        v-model="warningSearch"
        placeholder="预警搜索"
        prefix-icon="Search"
        class="warning-search"
      />
      <el-menu
        :default-active="activeMenu"
        class="category-menu"
      >
        <el-menu-item index="centralAsia">
          <el-icon><Location /></el-icon>
          <span>中亚政治</span>
        </el-menu-item>
        <!-- 可根据需要添加更多分类菜单项 -->
      </el-menu>
    </div>

    <!-- 右侧内容区（当前为空白，可根据需求填充） -->
    <div class="right-content">
      <!-- 这里可以放置右侧的预警相关内容 -->
    </div>

    <!-- 新增预警弹窗（右侧滑出） -->
    <el-drawer
      v-model="showAddWarningDialog"
      title="新增预警"
      direction="rtl"
      size="40%"
      :before-close="handleClose"
      class="add-warning-drawer"
    >
      <el-form :model="form" label-width="100px" class="warning-form">
        <el-form-item label="预警名称" required>
          <el-input
            v-model="form.warningName"
            placeholder="请输入预警名称"
            class="form-input"
          />
        </el-form-item>
        <el-form-item label="所属类别" required>
          <el-select
            v-model="form.category"
            placeholder="请选择类别名称"
            class="form-select"
          >
            <el-option
              v-for="item in categoryOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <el-button
            type="text"
            class="add-category-btn"
            @click="handleAddCategory"
          >
            <el-icon><Plus /></el-icon> 添加分类
          </el-button>
        </el-form-item>
        <el-form-item label="必须包含关键词">
          <el-input
            v-model="form.mustKeywords"
            placeholder="按Enter键对输入框进行赋值"
            type="textarea"
            rows="3"
            class="form-textarea"
          />
        </el-form-item>
        <el-form-item label="任意包含关键词">
          <el-input
            v-model="form.anyKeywords"
            placeholder="按Enter键对输入框进行赋值"
            type="textarea"
            rows="3"
            class="form-textarea"
          />
        </el-form-item>
        <el-form-item label="屏蔽歧义词">
          <el-input
            v-model="form.shieldWords"
            placeholder="按Enter键对输入框进行赋值"
            type="textarea"
            rows="3"
            class="form-textarea"
          />
        </el-form-item>
      </el-form>

      <div class="dialog-footer">
        <el-button @click="showAddWarningDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus,  Location } from '@element-plus/icons-vue'

// 控制弹窗显示
const showAddWarningDialog = ref(false)
// 预警搜索值
const warningSearch = ref('')
// 当前激活的菜单
const activeMenu = ref('centralAsia')

// 表单数据
const form = ref({
  warningName: '',
  category: '',
  mustKeywords: '',
  anyKeywords: '',
  shieldWords: ''
})

// 类别选项（示例数据）
const categoryOptions = ref([
  { label: '中亚政治', value: 'centralAsiaPolitics' },
  { label: '经济预警', value: 'economicWarning' },
  { label: '安全预警', value: 'safetyWarning' }
])

// 关闭弹窗回调
const handleClose = (done) => {
  // 可添加确认逻辑
  done()
}

// 提交表单
const handleSubmit = () => {
  // 实际项目中添加表单验证和接口请求
  console.log('提交预警数据:', form.value)
  showAddWarningDialog.value = false
}

// 新增分类（示例方法）
const handleAddCategory = () => {
  console.log('新增分类逻辑')
  // 可打开新的弹窗处理新增分类
}
</script>

<style scoped>
.warning-management-page {
  display: flex;
  height: 100vh;
  background-color: #e6f2ff;
  position: relative;
  top: 60px;
}

.left-sidebar {
  width: 200px;
  background-color: #fff;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  border-right: 1px solid #e5e7eb;
}

.add-warning-btn {
  width: 100%;
}

.warning-search {
  width: 100%;
}

.category-menu {
  flex: 1;
}

.right-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.add-warning-drawer {
  /* 确保弹窗层级足够高，覆盖可能存在的其他元素 */
  z-index: 200 !important;
}

.warning-form {
  margin-top: 20px;
}

.form-input,
.form-select {
  width: 100%;
  max-width: 350px;
}

.form-textarea {
  width: 100%;
  max-width: 350px;
}

.add-category-btn {
  margin-left: 10px;
}

.dialog-footer {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>

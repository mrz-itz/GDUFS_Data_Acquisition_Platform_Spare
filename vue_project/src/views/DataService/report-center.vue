<template>
  <div class="page-container">
    <!-- 主体内容区（作为导航栏的子组件） -->
    <div class="content-wrapper">
      <!-- 左侧分类栏 -->
      <div class="left-sidebar">
        <el-button
          type="primary"
          @click="showAddDialog = true"
          class="add-category-btn"
        >
          <el-icon><Plus /></el-icon> 新增分类
        </el-button>
        <el-input
          v-model="categorySearch"
          placeholder="分类搜索"
          prefix-icon="Search"
          class="category-search"
        />
      </div>

      <!-- 右侧内容区 -->
      <div class="right-content">
        <!-- 筛选区域 -->
        <div class="filter-bar">
          <el-input
            placeholder="请输入关键词"
            prefix-icon="Edit"
            class="keyword-input"
          />
          <el-date-picker
            type="date"
            placeholder="开始日期"
            class="date-picker"
          />
          <span class="date-separator">至</span>
          <el-date-picker
            type="date"
            placeholder="结束日期"
            class="date-picker"
          />
          <el-button type="primary" class="search-btn">
            <el-icon><Search /></el-icon> 搜索
          </el-button>
        </div>

        <!-- 数据表格 -->
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          empty-text="暂无数据"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="reportName" label="报告名称" />
          <el-table-column prop="keywords" label="关键词" />
          <el-table-column prop="queryTime" label="查询时间段" />
          <el-table-column prop="status" label="状态" />
          <el-table-column prop="createTime" label="新增时间" />
          <el-table-column label="操作" width="120">
            <template #default>
              <el-button type="text">编辑</el-button>
              <el-button type="text">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 右侧滑出弹窗（z-index 高于导航栏） -->
    <el-drawer
      v-model="showAddDialog"
      title="新增分类"
      direction="rtl"
      size="35%"
      class="category-drawer"
      :before-close="handleClose"
    >
      <el-form :model="form" label-width="100px" class="category-form">
        <el-form-item label="分类名称" required>
          <el-input
            v-model="form.categoryName"
            placeholder="请输入分类名称"
            class="form-input"
          />
        </el-form-item>
        <el-form-item label="所属父类">
          <el-select
            v-model="form.parentId"
            placeholder="请选择父类"
            class="form-select"
          >
            <el-option
              v-for="item in parentOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
          <el-button
            type="text"
            class="inline-add-btn"
            @click="handleAddParent"
          >
            <el-icon><Plus /></el-icon> 新增父类
          </el-button>
        </el-form-item>
        <el-form-item label="分类描述">
          <el-input
            v-model="form.description"
            placeholder="请输入分类描述（选填）"
            type="textarea"
            rows="3"
            class="form-textarea"
          />
        </el-form-item>
      </el-form>

      <div class="dialog-footer">
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确认提交</el-button>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus, Search,  } from '@element-plus/icons-vue'

// 控制弹窗显示
const showAddDialog = ref(false)
// 分类搜索值
const categorySearch = ref('')
// 表格数据（空数据）
const tableData = ref([])
// 表单数据
const form = ref({
  categoryName: '',
  parentId: '',
  description: ''
})
// 父类选项（示例数据）
const parentOptions = ref([
  { id: 1, name: '默认分类' },
  { id: 2, name: '系统分类' }
])

// 关闭弹窗回调
const handleClose = (done) => {
  // 可添加确认逻辑
  done()
}

// 提交表单
const handleSubmit = () => {
  // 实际项目中添加表单验证和接口请求
  console.log('提交分类数据:', form.value)
  showAddDialog.value = false
}

// 新增父类（示例方法）
const handleAddParent = () => {
  console.log('新增父类逻辑')
  // 可打开新的弹窗处理新增父类
}
</script>

<style scoped>
.page-container {
  /* 继承父组件（导航栏）的布局，作为子组件填充剩余空间 */
  height: calc(100vh - 60px); /* 假设导航栏高度为60px */
  display: flex;
  overflow: hidden;
}

.content-wrapper {
  display: flex;
  width: 100%;
  height: 100%;
}

/* 左侧分类栏 */
.left-sidebar {
  width: 220px;
  padding: 20px;
  border-right: 1px solid #e5e7eb;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.add-category-btn {
  width: 100%;
}

.category-search {
  width: 100%;
}

/* 右侧内容区 */
.right-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
  overflow-y: auto;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.keyword-input {
  width: 220px;
}

.date-picker {
  width: 160px;
}

.date-separator {
  color: #666;
}

.search-btn {
  display: flex;
  align-items: center;
}

/* 弹窗样式（核心：z-index 高于导航栏） */
.category-drawer {
  /* 假设导航栏z-index为100，弹窗设为200确保覆盖 */
  z-index: 200 !important;
}

/* 表单样式 */
.category-form {
  margin-top: 20px;
}

.form-input,
.form-select {
  width: 100%;
  max-width: 300px;
}

.form-textarea {
  width: 100%;
  max-width: 300px;
}

.inline-add-btn {
  margin-left: 10px;
}

.dialog-footer {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>

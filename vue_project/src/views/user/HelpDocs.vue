<template>
  <div class="help-docs-page">
    <div class="page-header">
      <h1 class="page-title">帮助文档</h1>
      <p class="page-subtitle">网页操作说明与平台功能介绍，供日常使用参考</p>
    </div>

    <div class="content-container">
      <section class="content-section">
        <h2 class="section-title">一、首页与导航</h2>
        <div class="section-card">
          <p>首页展示四大模块入口：<strong>舆情分析系统</strong>、<strong>开源计算平台</strong>、<strong>学术数据导航</strong>、<strong>数据服务系统</strong>。点击对应卡片即可进入。</p>
          <p>顶部导航栏提供：数据服务（含数据搜索、预警中心、报告中心、数据统计）、用户中心（需登录）、关于我们。右侧有搜索与用户中心快捷入口。</p>
        </div>
      </section>

      <section class="content-section">
        <h2 class="section-title">二、数据服务</h2>
        <div class="section-card">
          <h3>数据搜索</h3>
          <p>支持按主题、必须包含、任意包含、需要排除等条件检索新闻；可筛选发布时间、命中位置（全文/标题/摘要/正文）、数据源、语言。点击「搜索」执行查询，结果列表中可「查看详情」阅读正文，或「查看原文」跳转至来源链接。</p>
        </div>
        <div class="section-card">
          <h3>数据统计</h3>
          <p>展示新闻总数、语种数、新闻排行榜、多语言占比、媒体来源、信源类型等统计图表，可按时间范围切换查看。</p>
        </div>
        <div class="section-card">
          <h3>预警中心与报告中心</h3>
          <p>用于预警管理与报告查看，具体功能以实际页面为准。</p>
        </div>
      </section>

      <section class="content-section">
        <h2 class="section-title">三、舆情分析系统</h2>
        <div class="section-card">
          <p>提供舆情指数折线图，可设置起始日期与视距（近 7 天/1 个月/3 个月/全年）。点击图表数据点可打开侧边栏查看下钻分析。支持检索目标、事件、关键字进行筛选。</p>
        </div>
      </section>

      <section class="content-section">
        <h2 class="section-title">四、用户中心</h2>
        <div class="section-card">
          <h3>登录与退出</h3>
          <p>未登录时，导航栏显示「登录」。点击后输入用户名与密码，提交即可登录；登录成功后将跳转至原访问页或首页。</p>
          <p>登录后，导航栏显示「用户中心」下拉菜单，内含个人中心、我的应用、帮助文档、我的收录、<strong>退出登录</strong>。点击「退出登录」将清除登录状态并跳转至首页。</p>
        </div>
        <div class="section-card">
          <h3>个人中心、我的应用、我的收录</h3>
          <p>在用户中心下拉中进入对应子页，管理个人信息、应用与收藏内容。</p>
        </div>
      </section>

      <section class="content-section">
        <h2 class="section-title">五、关于我们</h2>
        <div class="section-card">
          <p>点击导航栏「关于我们」可查看平台与实验室介绍、联系方式等信息。</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.help-docs-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 20px;
  background: #fafafa;
  min-height: 100%;
}
.page-header {
  text-align: center;
  margin-bottom: 32px;
}
.page-title {
  font-size: 1.75rem;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}
.page-subtitle {
  font-size: 0.95rem;
  color: #666;
  margin: 0;
}
.content-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  padding: 32px;
}
.content-section {
  margin-bottom: 28px;
}
.content-section:last-child {
  margin-bottom: 0;
}
.section-title {
  font-size: 1.15rem;
  color: #333;
  margin: 0 0 12px 0;
  padding-bottom: 6px;
  border-bottom: 1px solid #eee;
}
.section-card {
  background: #fafafa;
  border-radius: 6px;
  padding: 16px 20px;
  margin-bottom: 12px;
}
.section-card:last-child {
  margin-bottom: 0;
}
.section-card h3 {
  font-size: 1rem;
  color: #444;
  margin: 0 0 8px 0;
}
.section-card p {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #555;
  margin: 0 0 8px 0;
}
.section-card p:last-child {
  margin-bottom: 0;
}
</style>

<script setup>
import { onMounted, onActivated, onUnmounted, nextTick, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const pageContainer = ref(null)

// 重置滚动位置到顶部
const resetScrollPosition = () => {
  // 重置window滚动位置
  window.scrollTo(0, 0)

  // 重置容器内部滚动位置
  nextTick(() => {
    if (pageContainer.value) {
      pageContainer.value.scrollTop = 0
    }
    // 再次确保window滚动位置为0
    window.scrollTo(0, 0)
  })
}

// 处理浏览器返回/前进按钮
const handlePopState = () => {
  // 延迟执行，确保页面已渲染
  setTimeout(() => {
    resetScrollPosition()
  }, 100)
}

// 组件挂载时重置滚动位置
onMounted(() => {
  // 禁用浏览器的自动滚动恢复
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual'
  }

  // 重置滚动位置
  resetScrollPosition()

  // 监听浏览器历史记录导航（返回/前进按钮）
  window.addEventListener('popstate', handlePopState)

  // 使用nextTick确保DOM已渲染后再重置一次
  nextTick(() => {
    resetScrollPosition()
  })
})

// 如果使用了keep-alive，在激活时也重置滚动位置
onActivated(() => {
  resetScrollPosition()
})

// 组件卸载时清理事件监听器
onUnmounted(() => {
  window.removeEventListener('popstate', handlePopState)
})
</script>

<template>
  <div class="about-us-page" ref="pageContainer">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">关于我们</h1>
      <p class="page-subtitle">广东外语外贸大学数据挖掘实验室（现 "蒋盛益创新工作室"）</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-container">
      <!-- 简介卡片 -->
      <div class="intro-card">
        <div class="card-icon">🏛️</div>
        <p class="intro-text">
          广东外语外贸大学数据挖掘实验室（现 "蒋盛益创新工作室"）是广外信息科学与技术学院（网络空间安全学院）的核心科研与人才培养平台，成立于 2006 年 10 月，由蒋盛益教授领衔，是外语类高校中极具特色的 "计算机 + 外语 + 大数据" 交叉创新团队。
        </p>
      </div>

      <!-- 一、基本概况 -->
      <section class="content-section">
        <div class="section-header">
          <span class="section-number">01</span>
          <h2 class="section-title">基本概况</h2>
        </div>
        <div class="section-content">
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">定位</div>
              <div class="info-value">教师引导、学生自主管理的创新型科研组织，以学术科研为主导，聚焦数据挖掘与自然语言处理技术的基础研究与应用落地。</div>
            </div>
            <div class="info-item">
              <div class="info-label">规模</div>
              <div class="info-value">现有学生成员 125 人，设 9 个研究小组；累计毕业 330 余名优秀学生，推动学院 13 个学生科技团队、2 个创新创业实践团队建设，覆盖全院近 50% 在校生。</div>
            </div>
            <div class="info-item">
              <div class="info-label">特色</div>
              <div class="info-value">依托广外外语与国际化优势，深耕 "多语种 + 数据智能" 交叉领域，是文科高校新工科人才培养的典型样本。</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 二、核心研究方向 -->
      <section class="content-section">
        <div class="section-header">
          <span class="section-number">02</span>
          <h2 class="section-title">核心研究方向</h2>
        </div>
        <div class="section-content">
          <div class="research-grid">
            <div class="research-card">
              <div class="research-icon">🔬</div>
              <h3 class="research-title">数据挖掘基础理论</h3>
              <p class="research-desc">聚类、分类、关联规则、异常检测等算法研究</p>
            </div>
            <div class="research-card">
              <div class="research-icon">💬</div>
              <h3 class="research-title">自然语言处理（NLP）</h3>
              <p class="research-desc">多语种文本分析、情感计算、低资源语言处理、文本生成与摘要</p>
            </div>
            <div class="research-card">
              <div class="research-icon">📊</div>
              <h3 class="research-title">网络文本与舆情分析</h3>
              <p class="research-desc">热点话题检测、公共事件舆情预警、观点挖掘</p>
            </div>
            <div class="research-card">
              <div class="research-icon">🌐</div>
              <h3 class="research-title">社会网络分析</h3>
              <p class="research-desc">网络可视化、链路预测、群体行为建模</p>
            </div>
            <div class="research-card">
              <div class="research-icon">🎯</div>
              <h3 class="research-title">个性化推荐系统</h3>
              <p class="research-desc">电商 / 新闻 / 教育场景的智能推荐、可监管推荐算法</p>
            </div>
            <div class="research-card">
              <div class="research-icon">🔍</div>
              <h3 class="research-title">企业竞争情报</h3>
              <p class="research-desc">多语种情报提取、行业态势推理、跨境数据应用</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 三、核心师资团队 -->
      <section class="content-section">
        <div class="section-header">
          <span class="section-number">03</span>
          <h2 class="section-title">核心师资团队</h2>
        </div>
        <div class="section-content">
          <div class="team-info">
            <p class="team-lead">
              由<strong>蒋盛益教授</strong>（实验室创始人、学科带头人）领衔，核心成员包括：
            </p>
            <ul class="team-list">
              <li><strong>王连喜教授</strong>：NLP 与多语种智能信息处理专家，主持多项国家社科、省部级项目</li>
              <li><strong>肖锋、丘心颖、姜思羽、颜学明、张新猛</strong>等副教授 / 讲师，覆盖数据挖掘、机器学习、网络安全等方向</li>
            </ul>
            <p class="team-note">
              团队长期深耕 "一带一路"、粤港澳大湾区相关的多语种数据智能研究，科研与项目经验丰富。
            </p>
          </div>
        </div>
      </section>

      <!-- 四、近年核心成就 -->
      <section class="content-section">
        <div class="section-header">
          <span class="section-number">04</span>
          <h2 class="section-title">近年核心成就（2019-2026）</h2>
        </div>
        <div class="section-content">
          <div class="achievement-tabs">
            <div class="achievement-item">
              <div class="achievement-icon">📝</div>
              <h3 class="achievement-title">学术成果（高水平论文）</h3>
              <ul class="achievement-list">
                <li>累计发表学术论文 <strong>60 余篇</strong>，其中 SCI 收录 4 篇、EI 收录 12 篇、CSCD/CSSCI 论文 37 篇</li>
                <li>2021 年：发表 / 录用高水平论文 <strong>18 篇</strong>，申请软著 / 专利 <strong>15 项</strong></li>
                <li>2024 年：本科生陈卓玮以第一作者在 <strong>EMNLP 2024</strong>（CCF B 类、NLP 顶级会议）发表论文</li>
                <li>多篇论文发表于《Information Sciences》（SCI Q1，IF=6.795）等国际权威期刊</li>
              </ul>
            </div>
            <div class="achievement-item">
              <div class="achievement-icon">🔬</div>
              <h3 class="achievement-title">科研项目（国家级 / 省部级）</h3>
              <ul class="achievement-list">
                <li>成员参与 <strong>5 项国家级科研项目</strong>、<strong>6 项省部级科研项目</strong></li>
                <li><strong>国家自然科学基金</strong>：面向中国英语学习者的英文作文全自动评分、无线网络资源优化机制研究</li>
                <li><strong>国家社科基金</strong>：东盟涉华舆情观点挖掘、"一带一路" 科技合作机理研究</li>
                <li><strong>广东省自然科学基金</strong>：基于 LDA 的可监管推荐系统、图卷积网络自动问答系统</li>
                <li><strong>广东省重点领域研发计划</strong>：自主可控联盟区块链关键技术研究</li>
              </ul>
            </div>
            <div class="achievement-item">
              <div class="achievement-icon">💡</div>
              <h3 class="achievement-title">知识产权与技术成果</h3>
              <ul class="achievement-list">
                <li>累计申请<strong>软件著作权 20 项</strong>、<strong>专利 5 项</strong></li>
                <li>研发多语种舆情监测、跨境电商数据挖掘、教育智能评分等系统，服务政府与企业需求</li>
              </ul>
            </div>
            <div class="achievement-item">
              <div class="achievement-icon">🏆</div>
              <h3 class="achievement-title">学科竞赛（国际 / 国家级奖项）</h3>
              <ul class="achievement-list">
                <li>2015 年至今，获 <strong>"挑战杯"、泛三角计算机作品赛、全国大学生计算机大赛、粤港澳计算机作品赛等省级以上奖项 30 余项</strong></li>
                <li>2021 年：斩获 <strong>6 项国际级奖项</strong>、<strong>4 项国家级奖项</strong>、<strong>4 项省级奖项</strong></li>
                <li>多次在大数据、人工智能、软件设计类赛事中夺冠，如 <strong>2016 年厦门大数据大赛冠军</strong></li>
              </ul>
            </div>
            <div class="achievement-item">
              <div class="achievement-icon">⭐</div>
              <h3 class="achievement-title">荣誉称号</h3>
              <ul class="achievement-list">
                <li>2012 年：实验室团队获广外最高荣誉 <strong>"校长奖章"</strong></li>
                <li>2018 年：成员林楠铠获广外 <strong>"校长奖章"</strong></li>
                <li>2021 年：实验室升级为 <strong>"蒋盛益创新工作室"</strong>，获评<strong>广东省劳模和工匠人才创新工作室</strong></li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- 五、人才培养成果 -->
      <section class="content-section">
        <div class="section-header">
          <span class="section-number">05</span>
          <h2 class="section-title">人才培养成果</h2>
        </div>
        <div class="section-content">
          <div class="talent-grid">
            <div class="talent-card">
              <div class="talent-number">30+</div>
              <div class="talent-label">升学深造</div>
              <div class="talent-desc">近 30 人赴国内外攻读硕士（推免 14 人），多名学生获广州市菁英计划资助赴英、美等国名校深造</div>
            </div>
            <div class="talent-card">
              <div class="talent-number">10+</div>
              <div class="talent-label">国家奖学金</div>
              <div class="talent-desc">累计获国家奖学金 10 余人次</div>
            </div>
            <div class="talent-card">
              <div class="talent-number">20+</div>
              <div class="talent-label">学生项目</div>
              <div class="talent-desc">学生主持省级以上学术研究项目 20 余项</div>
            </div>
            <div class="talent-card">
              <div class="talent-icon">💼</div>
              <div class="talent-label">就业质量</div>
              <div class="talent-desc">毕业生进入腾讯、阿里、华为、百度、金融机构、政府部门等，从事数据挖掘、算法研发、NLP 工程师等岗位</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 六、社会影响与特色价值 -->
      <section class="content-section">
        <div class="section-header">
          <span class="section-number">06</span>
          <h2 class="section-title">社会影响与特色价值</h2>
        </div>
        <div class="section-content">
          <div class="impact-grid">
            <div class="impact-card">
              <div class="impact-icon">🚀</div>
              <h3 class="impact-title">交叉创新标杆</h3>
              <p class="impact-desc">开创 "计算机 + 外语 + 大数据" 培养模式，实现教学组织、方式、模式的 "三个转变"，为文科高校新工科建设提供范本</p>
            </div>
            <div class="impact-card">
              <div class="impact-icon">🌏</div>
              <h3 class="impact-title">服务国家战略</h3>
              <p class="impact-desc">围绕 "一带一路""粤港澳大湾区"，开展多语种舆情、跨境数据、科技合作等研究，支撑区域与国家数字化发展</p>
            </div>
            <div class="impact-card">
              <div class="impact-icon">🤝</div>
              <h3 class="impact-title">产学研融合</h3>
              <p class="impact-desc">与企业合作研发智能系统，将科研成果转化为实际应用，提升技术落地能力</p>
            </div>
            <div class="impact-card">
              <div class="impact-icon">✨</div>
              <h3 class="impact-title">示范引领</h3>
              <p class="impact-desc">作为学院科创核心平台，带动全院学生科创氛围，成为广外信息学科的标志性团队</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
/* ==================== 主容器样式 ==================== */
.about-us-page {
  position: fixed;
  top: 60px; /* 导航栏高度 */
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  overflow-y: auto;
  padding: 0;
}

/* ==================== 页面头部 ==================== */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 40px 60px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
  opacity: 0.3;
}

.page-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin: 0 0 16px 0;
  position: relative;
  z-index: 1;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  letter-spacing: 2px;
}

.page-subtitle {
  font-size: 1.3rem;
  margin: 0;
  opacity: 0.95;
  position: relative;
  z-index: 1;
  font-weight: 300;
}

/* ==================== 内容容器 ==================== */
.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* ==================== 简介卡片 ==================== */
.intro-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  margin-bottom: 60px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border-left: 4px solid #667eea;
  display: flex;
  gap: 24px;
  align-items: flex-start;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.intro-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
}

.card-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.intro-text {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
  margin: 0;
  flex: 1;
}

/* ==================== 内容区块样式 ==================== */
.content-section {
  margin-bottom: 80px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 3px solid #667eea;
}

.section-number {
  font-size: 3rem;
  font-weight: 900;
  color: #667eea;
  opacity: 0.2;
  line-height: 1;
}

.section-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

/* ==================== 信息网格 ==================== */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.info-item {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  border-top: 3px solid #667eea;
}

.info-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.info-label {
  font-size: 1.1rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 12px;
}

.info-value {
  font-size: 0.95rem;
  line-height: 1.7;
  color: #555;
}

/* ==================== 研究方向网格 ==================== */
.research-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.research-card {
  background: white;
  padding: 32px 24px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.research-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.research-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.research-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.research-desc {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #666;
  margin: 0;
}

/* ==================== 团队信息 ==================== */
.team-info {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.team-lead {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
  margin-bottom: 24px;
}

.team-lead strong {
  color: #667eea;
  font-size: 1.2rem;
}

.team-list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
}

.team-list li {
  padding: 16px 0;
  padding-left: 32px;
  position: relative;
  font-size: 1rem;
  line-height: 1.8;
  color: #555;
  border-bottom: 1px solid #f0f0f0;
}

.team-list li:last-child {
  border-bottom: none;
}

.team-list li::before {
  content: '👤';
  position: absolute;
  left: 0;
  top: 16px;
  font-size: 1.2rem;
}

.team-list li strong {
  color: #667eea;
}

.team-note {
  font-size: 1rem;
  line-height: 1.8;
  color: #666;
  font-style: italic;
  margin: 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

/* ==================== 成就展示 ==================== */
.achievement-tabs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

.achievement-item {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  border-top: 4px solid #667eea;
}

.achievement-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.achievement-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
}

.achievement-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 20px 0;
}

.achievement-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.achievement-list li {
  padding: 12px 0;
  padding-left: 24px;
  position: relative;
  font-size: 0.95rem;
  line-height: 1.7;
  color: #555;
  border-bottom: 1px solid #f5f5f5;
}

.achievement-list li:last-child {
  border-bottom: none;
}

.achievement-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  top: 12px;
  color: #667eea;
  font-weight: bold;
  font-size: 1.1rem;
}

.achievement-list li strong {
  color: #667eea;
  font-weight: 700;
}

/* ==================== 人才培养网格 ==================== */
.talent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.talent-card {
  background: white;
  padding: 32px 24px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.talent-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.talent-number {
  font-size: 3.5rem;
  font-weight: 900;
  color: #667eea;
  line-height: 1;
  margin-bottom: 12px;
}

.talent-icon {
  font-size: 3rem;
  margin-bottom: 12px;
}

.talent-label {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 12px;
}

.talent-desc {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #666;
  margin: 0;
}

/* ==================== 社会影响网格 ==================== */
.impact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.impact-card {
  background: white;
  padding: 32px 24px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.impact-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.impact-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.impact-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 16px 0;
}

.impact-desc {
  font-size: 0.95rem;
  line-height: 1.7;
  color: #666;
  margin: 0;
}

/* ==================== 响应式设计 ==================== */
@media (max-width: 768px) {
  .page-title {
    font-size: 2.5rem;
  }

  .page-subtitle {
    font-size: 1.1rem;
  }

  .content-container {
    padding: 40px 20px;
  }

  .intro-card {
    flex-direction: column;
    padding: 24px;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .section-number {
    font-size: 2rem;
  }

  .info-grid,
  .research-grid,
  .achievement-tabs,
  .talent-grid,
  .impact-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

// 当前选中的标签
const activeTab = ref('algorithm')

// 切换标签
const switchTab = (tab) => {
  activeTab.value = tab
}

// 轮播图相关
const currentSlide = ref(0)
const carouselImages = ref([
  'imgs/openComputer/开源计算平台轮播图1.jpg',
  'imgs/openComputer/开源计算平台轮播图2.jpg',
  'imgs/openComputer/开源计算平台轮播图3.jpg',
  'imgs/openComputer/开源计算平台轮播图4.jpg',
])

// 带克隆项的列表（在末尾克隆第一张，在开头克隆最后一张）
const slidesWithClone = computed(() => {
  if (carouselImages.value.length === 0) return []
  const list = [carouselImages.value[carouselImages.value.length - 1]] // 克隆最后一张到开头
  return list.concat(carouselImages.value, [carouselImages.value[0]]) // 克隆第一张到末尾
})

// 根据总帧数计算需要平移的百分比（相对 track 自身宽度）
const trackTranslatePercent = computed(() => {
  return currentSlide.value * 100
})

// 控制是否启用过渡（用于无缝重置）
const enableTransition = ref(true)

let carouselTimer = null

// 自动轮播
const startCarousel = () => {
  stopCarousel()
  carouselTimer = setInterval(() => {
    nextSlide()
  }, 2500)
}

// 停止轮播
const stopCarousel = () => {
  if (carouselTimer) {
    clearInterval(carouselTimer)
    carouselTimer = null
  }
}

// 手动切换到指定图片（真实索引）
const goToSlide = (index) => {
  enableTransition.value = true
  currentSlide.value = index + 1
}

// 上一张（无缝）
const prevSlide = () => {
  enableTransition.value = true
  currentSlide.value -= 1
}

// 下一张（无缝）
const nextSlide = () => {
  enableTransition.value = true
  currentSlide.value += 1
}

// 过渡结束时的无缝重置
const handleTransitionEnd = () => {
  if (currentSlide.value === carouselImages.value.length + 1) {
    enableTransition.value = false
    currentSlide.value = 1
    setTimeout(() => {
      enableTransition.value = true
    }, 0)
  } else if (currentSlide.value === 0) {
    enableTransition.value = false
    currentSlide.value = carouselImages.value.length
    setTimeout(() => {
      enableTransition.value = true
    }, 0)
  }
}

// 组件挂载时开始轮播
onMounted(() => {
  currentSlide.value = 1
  startCarousel()
})

// 组件卸载时停止轮播
onUnmounted(() => {
  stopCarousel()
})

// 算法超市数据
const algorithms = [
  {
    id: 1,
    name: '情感分析',
    description:
      '利用自然语言处理和文本挖掘技术，对带有情感色彩的主观性文本进行情感倾向性分析，识别文本中的情感态度和情绪状态。',
  },
  {
    id: 2,
    name: '文本分析',
    description:
      '文本挖掘、信息检索的一个基本问题，它把从文本中抽取出的特征词进行量化来表示文本信息，实现文本的自动分类和聚类。',
  },
  {
    id: 3,
    name: '人脸识别',
    description:
      '基于人的脸部特征信息进行身份识别的一种生物识别技术，通过分析人脸图像中的特征点来实现身份验证和识别。',
  },
  {
    id: 4,
    name: '生存分析',
    description:
      '生存分析的主要目的就是研究与分析死亡速度、生存率(死亡率)、生存时间等指标，评估不同因素对生存时间的影响。',
  },
  {
    id: 5,
    name: '聚类分析',
    description:
      '聚类分析的目标就是在相似的基础上收集数据来分类，将相似的对象归为一类，不同类的对象之间差异较大。',
  },
  {
    id: 6,
    name: '回归分析',
    description:
      '确定两种或两种以上变量间相互依赖的定量关系的一种统计分析方法，用于预测和解释变量之间的关系。',
  },
  {
    id: 7,
    name: '相似检测',
    description:
      '基于关键词匹配的传统方法结合向量空间和深度学习进行文本相似度检测，识别文档间的相似性和重复内容。',
  },
]
</script>

<template>
  <div class="open-computing">
    <!-- 轮播图区域 -->
    <div class="carousel-container" @mouseenter="stopCarousel" @mouseleave="startCarousel">
      <div class="carousel-wrapper">
        <div
          class="carousel-slides"
          :style="{
            transform: `translateX(-${trackTranslatePercent}%)`,
            transition: enableTransition ? 'transform 0.5s ease-in-out' : 'none',
          }"
          @transitionend="handleTransitionEnd"
        >
          <div v-for="(image, index) in slidesWithClone" :key="index" class="carousel-slide">
            <img :src="image" :alt="`轮播图 ${index}`" class="carousel-image" />
          </div>
        </div>

        <!-- 左右切换按钮 -->
        <button class="carousel-btn carousel-btn-prev" @click="prevSlide">
          <span>‹</span>
        </button>
        <button class="carousel-btn carousel-btn-next" @click="nextSlide">
          <span>›</span>
        </button>

        <!-- 指示器 -->
        <div class="carousel-indicators">
          <button
            v-for="(image, index) in carouselImages"
            :key="index"
            :class="['indicator', {
              active: currentSlide === index + 1 ||
                     (currentSlide === 0 && index === carouselImages.length - 1) ||
                     (currentSlide === carouselImages.length + 1 && index === 0)
            }]"
            @click="goToSlide(index)"
          ></button>
        </div>
      </div>
    </div>

    <!-- 功能切换标签 -->
    <div class="tab-container">
      <div class="tabs">
        <button
          :class="['tab-button', { active: activeTab === 'algorithm' }]"
          @click="switchTab('algorithm')"
        >
          算法超市
        </button>
        <button
          :class="['tab-button', { active: activeTab === 'deployment' }]"
          @click="switchTab('deployment')"
        >
          模型部署
        </button>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-area">
      <div v-if="activeTab === 'algorithm'" class="algorithm-supermarket">
        <div class="algorithm-grid">
          <div v-for="algorithm in algorithms" :key="algorithm.id" class="algorithm-card">
            <h3>{{ algorithm.name }}</h3>
            <p>{{ algorithm.description }}</p>
            <div class="card-actions">
              <button class="use-btn">立即使用</button>
              <button class="detail-btn">查看详情</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'deployment'" class="model-deployment">
        <div class="deployment-content">
          <h2>模型部署</h2>
          <p>模型部署功能正在开发中...</p>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <div class="footer">
      <p>地址：广东外语外贸大学数据挖掘实验室 邮箱：阿巴阿巴.cn 版权所有</p>
    </div>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 核心修改1：使用固定定位，避免滚动条影响导航栏 */
.open-computing {
  position: fixed;
  top: 60px; /* 导航栏下方 */
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  /* 允许内部内容滚动 */
  overflow-y: auto;
  /* 移除 padding-top，因为已经通过 top: 60px 定位了 */
  padding-top: 0;
}

/* 轮播图区域 */
.carousel-container {
  width: 100%;
  height: 400px;
  overflow: hidden;
  position: relative;
  background: #000;
}

.carousel-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.carousel-slides {
  display: flex;
  width: 100%;
  height: 100%;
  transition: transform 0.5s ease-in-out;
}

.carousel-slide {
  flex: 0 0 100%;
  width: 100%;
  height: 100%;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 左右切换按钮 */
.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 24px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
}

.carousel-btn:hover {
  background: rgba(0, 0, 0, 0.8);
  transform: translateY(-50%) scale(1.1);
}

.carousel-btn-prev {
  left: 20px;
}

.carousel-btn-next {
  right: 20px;
}

/* 指示器 */
.carousel-indicators {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 10;
}

.indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator.active {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.2);
}

.indicator:hover {
  background: rgba(255, 255, 255, 0.8);
}

/* 功能切换标签 - 核心修改2：优化sticky定位和层级 */
.tab-container {
  background: white;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  /* 关键：sticky定位到视口顶部（导航栏下方） */
  position: sticky;
  top: 0;
  /* 层级高于页面内容，低于导航栏（导航栏z-index=20） */
  z-index: 10;
  width: 100%;
  box-sizing: border-box;
  /* 确保背景不透明，防止内容穿透 */
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.tabs {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
}

.tab-button {
  padding: 20px 40px;
  border: none;
  background: transparent;
  font-size: 18px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.tab-button:hover {
  color: #667eea;
}

.tab-button.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

/* 内容区域 */
.content-area {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 算法超市 */
.algorithm-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
  margin-top: 20px;
}

.algorithm-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #e8e8e8;
}

.algorithm-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.algorithm-card h3 {
  color: #333;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
}

.algorithm-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
  font-size: 14px;
}

.card-actions {
  display: flex;
  gap: 12px;
}

.use-btn,
.detail-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.use-btn {
  background: #667eea;
  color: white;
}

.use-btn:hover {
  background: #5a6fd8;
}

.detail-btn {
  background: transparent;
  color: #667eea;
  border: 1px solid #667eea;
}

.detail-btn:hover {
  background: #667eea;
  color: white;
}

/* 模型部署 */
.model-deployment {
  text-align: center;
  padding: 80px 20px;
}

.deployment-content h2 {
  color: #333;
  font-size: 32px;
  margin-bottom: 16px;
}

.deployment-content p {
  color: #666;
  font-size: 18px;
}

/* 页脚 */
.footer {
  background: #f8f9fa;
  padding: 20px;
  text-align: center;
  color: #666;
  font-size: 14px;
  border-top: 1px solid #e8e8e8;
  margin-top: 40px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .carousel-container {
    height: 250px;
  }

  .carousel-btn {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .carousel-btn-prev {
    left: 10px;
  }

  .carousel-btn-next {
    right: 10px;
  }

  .carousel-indicators {
    bottom: 15px;
  }

  .indicator {
    width: 10px;
    height: 10px;
  }

  .algorithm-grid {
    grid-template-columns: 1fr;
  }

  .tabs {
    justify-content: center;
  }

  .tab-button {
    padding: 16px 24px;
    font-size: 16px;
  }
}
</style>

<!-- src/views/appHome.vue -->
<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goTo = (path) => {
  router.push(`/${path}`)
}
</script>

<template>
  <div class="home-container">
    <div class="main-content">
      <div class="card-group">
        <div class="card card-1" @click="goTo('sentiment-analysis')">

          <h3>舆情分析系统</h3>
          <p>实时监测全网舆情助力精准决策</p>
          <!-- 修改：span 替换为 button -->
          <button class="card-btn">立即进入</button>
        </div>
        <div class="card card-2" @click="goTo('open-computing')">
          <h3>开源计算平台</h3>
          <p>即选即用的预测算法模型封装</p>
          <button class="card-btn">立即进入</button>
        </div>
        <div class="card card-3" @click="goTo('academic-data')">
          <h3>学术数据导航</h3>
          <p>全球最全数据网站入口与使用指南</p>
          <button class="card-btn">立即进入</button>
        </div>
        <div class="card card-4" @click="goTo('data-service/data-search')">
          <h3>数据服务系统</h3>
          <p>汇集全球最快最全的新闻资讯</p>
          <button class="card-btn">立即进入</button>
        </div>
      </div>
    </div>
    <div class="footer">
      <p>地址：广东外语外贸大学数据挖掘实验室 邮箱：阿巴阿巴.cn 版权所有</p>
    </div>
  </div>
</template>

<style scoped>

.home-container {
  display: flex;
  flex-direction: column;

  margin: 0;
  padding: 0;

  min-height: 100vh;
  height: 100vh;
  width: 100%;
  padding-top: 0 !important;
  box-sizing: border-box;
  background-image: url('imgs/home/背景图.png');
  background-size: cover;

  background-position: center center;
  background-clip: border-box;
  background-repeat: no-repeat;

  padding-left: 0 !important;
  overflow: hidden;
}

.main-content {
  width: 1433px;
  margin: 160px auto 0;

  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
  padding-top: 0;
  margin-top: 0;
}

.card-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 64px 51px;
  margin-bottom: 0;

}

.card {
  /* width: 691px;
  height: 320px; */
  width: 620px;
  height: 290px;
  flex-shrink: 0;
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 5px 10px rgba(0, 102, 204, 0.12);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 102, 204, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 102, 204, 0.15);
}

.card h3 {
  font-size: 30px;
  color: rgba(33, 31, 35, 0.8);
  margin-bottom: 15px;
  font-weight: 600;
  z-index: 2;
  position: relative;
  top: 48px;
  left: 41px;
}

.card p {
  color: rgba(128, 128, 128, 1);
  margin-bottom: 20px;
  line-height: 1.6;
  font-size: 14px;
  flex-grow: 1;
  z-index: 2;
  position: relative;
  top: 50px;
  left:41px;
}

/* 新增：卡片按钮样式 */
.card-btn {
  background-color: rgba(0, 143, 252, 1);
  width: 80px;
  height: 38px;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 24px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2;
  position: relative;
  bottom: 54px;
  left: 41px;
  width: fit-content;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-btn:hover {
  background-color: #004c99;
  transform: translateY(-2px);
}

.card-1 {
  background-image: url('imgs/home/数据服务系统背景图.png');
  background-size: cover;
  background-position: center;
}

.card-2 {
  background-image: url('imgs/home/开源计算平台背景图.png');
  background-size: cover;
  background-position: center;
}

.card-3 {
  background-image: url('imgs/home/数据导航背景图.png');
  background-size: cover;
  background-position: center;
}

.card-4 {
  background-image: url('imgs/home/数据库产品背景图.png');
  background-size: cover;
  background-position: center;
}

.footer {
  position: relative;
  bottom: 60px;
  text-align: center;
  color: #666;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
  font-size: 15px;

  flex-shrink: 0;
  margin-top: 0;
}
</style>

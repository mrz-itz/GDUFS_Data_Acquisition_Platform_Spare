// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import appHome from '@/views/appHome.vue'
import DataSearch from '@/views/DataSearch.vue'
import OpenComputing from '@/views/OpenComputing.vue'
import AcademicData from '@/views/AcademicData.vue'
import DatabaseProduct from '@/views/sentimentAnalysis.vue'
import UserCenter from '@/views/UserCenter.vue'
import AboutUs from '@/views/AboutUs.vue'
import { getToken } from '@/utils/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { hideNavbar: true, public: true }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue'),
      meta: { hideNavbar: true, public: true }
    },
    {
      path: '/forgot-password',
      name: 'ForgotPassword',
      component: () => import('@/views/ForgotPassword.vue'),
      meta: { hideNavbar: true, public: true }
    },
    {
      path: '/reset-password',
      name: 'ResetPassword',
      component: () => import('@/views/ResetPassword.vue'),
      meta: { hideNavbar: true, public: true }
    },
    {
      path: '/',
      component: appHome,
      meta: {
        keepAlive: false, // 不缓存首页
        hideNavbar: false
      }
    },
    {
      path: '/data-service',
      component: DataSearch,
      children: [
        {
          path: 'data-search',
          name: 'DataSearch',
          component: () => import('@/views/DataService/data-search.vue')
        },
        {
          path: 'alert-center',
          name: 'AlertCenter',
          component: () => import('@/views/DataService/alert-center.vue')
        },
        {
          path: 'report-center',
          name: 'ReportCenter',
          component: () => import('@/views/DataService/report-center.vue')
        },
        {
          path: 'data-statistics',
          name: 'DataStatistics',
          component: () => import('@/views/DataService/data-statistics.vue'),
          meta: {
            hideNavbar: true,
            keepAlive: false
          }
        },
        {
          path: 'news/:id',
          name: 'NewsDetail',
          component: () => import('@/views/DataService/news-detail.vue')
        }
      ]
    },
    {
      path: '/open-computing',
      component: OpenComputing,
      meta: { hideNavbar: false }
    },
    {
      path: '/academic-data',
      component: AcademicData,
      meta: { hideNavbar: false }
    },
    {
      path: '/sentiment-analysis',
      component: DatabaseProduct,
      meta: { hideNavbar: false }
    },
    {
      path: '/user-center',
      component: UserCenter,
      meta: { requiresAuth: true, hideNavbar: false },
      children: [
          {
            path: 'personal-center',
            component: () => import('@/views/user/PersonalCenter.vue')
          },
          {
            path: 'my-applications',
            component: () => import('@/views/user/MyApplications.vue')
          },
          {
            path: 'help-docs',
            component: () => import('@/views/user/HelpDocs.vue')
          },
          {
            path: 'my-collections',
            component: () => import('@/views/user/MyCollections.vue')
          },
          {
            path: 'logout',
            component: () => import('@/views/user/Logout_.vue')
          }
      ]
    },
    {
      path: '/about-us',
      component: AboutUs,
      meta: { hideNavbar: false }
    }
  ],
})

// 添加全局路由守卫
router.beforeEach((to, from, next) => {
  const token = getToken()
  const requiresAuth = to.matched.some((record) => record.meta?.requiresAuth)
  if (requiresAuth && !token) {
    next({ path: '/login', query: { redirect: to.fullPath } })
    return
  }
  if (to.path === '/login' && token) {
    next(to.query.redirect || '/')
    return
  }
  if (to.path === '/' && from.path !== '/') {
    window.dispatchEvent(new CustomEvent('routeToHome'))
  }
  next()
})

export default router

/**
 * 统一 API 基地址配置，供 data-search、data-statistics 等使用
 */
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const API_PREFIX = `${BASE_URL}/api`

export { BASE_URL, API_PREFIX }

# 后台 API 说明

## 统一响应约定

- **成功**：直接返回业务 JSON，不包一层 `{ code, data }`。例如 `GET /api/dashboard/stats` 返回 `{ total_news, total_languages, language_stats }`。
- **错误**：使用 HTTP 状态码（如 401、500）和 FastAPI 默认格式 `{ "detail": "错误信息" }`。

## 主要接口

### 1. 分页列表（推荐替代原 titles/abstracts/pub-times/request-urls）

**GET /api/dashboard/news**

- 查询参数：`page`（默认 1）、`size`（默认 10，最大 100）、`sort_by`（默认 `pub_time`）、`sort_order`（默认 `desc`）。
- 响应示例：
```json
{
  "data": [
    {
      "id": 1,
      "title": "新闻标题",
      "abstract": "摘要",
      "pub_time": "2025-01-01 12:00:00",
      "request_url": "https://example.com/...",
      "language_id": 1,
      "source": "Example",
      "location": "中国"
    }
  ],
  "total": 1000,
  "page": 1,
  "page_size": 10,
  "total_pages": 100,
  "has_next": true,
  "has_prev": false
}
```

### 2. 条件搜索

**POST /api/dashboard/search**

- 请求体示例：
```json
{
  "keyword": "关键词",
  "must_include": "必须包含词",
  "any_include": "可选包含词",
  "need_exclude": "排除词",
  "hit_location": "全文",
  "publish_time": "近一月",
  "country": "中国",
  "page": 1,
  "page_size": 10,
  "sort_by": "pub_time",
  "sort_order": "desc"
}
```
- 响应除上述列表字段外多一个 `query_time_ms`（本次查询耗时毫秒）。

### 3. 认证

- **POST /api/auth/login**：请求体 `{ "username": "admin", "password": "admin" }`，成功返回 `{ "access_token": "JWT...", "token_type": "bearer" }`。
- **GET /api/auth/me**：请求头 `Authorization: Bearer <access_token>`，成功返回 `{ "username": "admin" }`。

## 环境变量（可选）

- `JWT_SECRET_KEY`：JWT 密钥，生产环境务必修改。
- `ADMIN_USER` / `ADMIN_PASSWORD`：登录账号密码，默认 admin/admin。

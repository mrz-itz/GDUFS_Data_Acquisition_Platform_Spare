from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from sqlalchemy import desc, or_, func, and_, not_, text, case
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, timezone
import models
from database import get_db, create_tables, SessionLocal, DB_HOST, DB_PORT, DB_NAME
from pydantic import BaseModel, ConfigDict, Field
import uvicorn
import os
import re
from urllib.parse import urlparse
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import json
from passlib.hash import bcrypt
import hashlib
import secrets
import smtplib
from email.message import EmailMessage

# 从 backend 目录加载 .env，使 DEEPSEEK_API_KEY 等环境变量生效
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


# ================== 生命周期管理 ==================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时尝试连接数据库，不仅是创建表
    try:
        create_tables()
        print(f"✅ 数据库连接成功，表检查完毕 -> {DB_HOST}:{DB_PORT}/{DB_NAME}")
        db = SessionLocal()
        try:
            news_cnt = db.execute(text("SELECT COUNT(*) FROM public.news")).scalar() or 0
            user_cnt = db.execute(text("SELECT COUNT(*) FROM public.app_user")).scalar() or 0
            print(f"📊 当前库概览: news={news_cnt}, app_user={user_cnt}")
            run_startup_schema_check(db)
        finally:
            db.close()
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
    yield


app = FastAPI(
    title="新闻爬虫数据API",
    description="从dg_dev_crawler数据库的news表读取数据的API服务",
    version="1.0.0",
    lifespan=lifespan
)

# ================== CORS配置 ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_startup_schema_check(db: Session):
    """启动只读自检：关键表与字段是否齐全。"""
    required_columns = {
        "news": {"id", "title", "abstract", "body", "pub_time", "request_url", "language_id"},
        "app_user": {"id", "username", "password_hash", "full_name", "email", "phone", "updated_at"},
        "language": {"id", "name"},
        "user_favorite": {"id", "user_id", "news_id"},
        "user_search_history": {"id", "user_id", "keyword"},
        "password_reset_token": {"id", "user_id", "token_hash", "expires_at", "used_at", "created_at"},
    }
    rows = db.execute(
        text(
            """
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name IN ('news', 'app_user', 'language', 'user_favorite', 'user_search_history', 'password_reset_token')
            """
        )
    ).fetchall()
    by_table: Dict[str, set[str]] = {}
    for table_name, column_name in rows:
        by_table.setdefault(table_name, set()).add(column_name)
    missing: Dict[str, List[str]] = {}
    for table_name, cols in required_columns.items():
        got = by_table.get(table_name, set())
        miss = sorted(cols - got)
        if miss:
            missing[table_name] = miss
    if missing:
        print(f"⚠️ schema 自检告警: {missing}")
    else:
        print("✅ schema 自检通过: 核心表字段齐全")


# ================== 数据模型 ==================

# 基础字段响应
class FieldResponse(BaseModel):
    id: int
    value: str
    model_config = ConfigDict(from_attributes=True)


class PaginatedFieldResponse(BaseModel):
    data: List[FieldResponse]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
    model_config = ConfigDict(from_attributes=True)


# 统计响应模型
class StatsResponse(BaseModel):
    total_news: int
    total_languages: int  # 新增：语言总数
    language_stats: List[Dict[str, Any]]


# 搜索请求参数
class SearchRequest(BaseModel):
    keyword: Optional[str] = None
    topic: Optional[str] = None
    must_include: Optional[str] = None
    any_include: Optional[str] = None
    need_exclude: Optional[str] = None
    publish_time: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    hit_location: Optional[str] = Field(
        default="全文",
        description='关键词匹配范围："全文"（title+abstract+body）、"标题"（title）、"摘要"（abstract）、"正文"（body）',
    )
    data_source: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None  # 与 country 二选一，均为 language 表 name
    site: Optional[str] = None
    page: int = 1
    page_size: int = 10
    sort_by: Optional[str] = "pub_time"
    sort_order: Optional[str] = "desc"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "keyword": "Philippine Independence",
                    "must_include": "Jeddah Consulate",
                    "any_include": "reception flag-raising",
                    "need_exclude": "spam",
                    "hit_location": "全文",
                    "publish_time": "近一月",
                    "country": "中国",
                    "data_source": "dfa.gov.ph",
                    "page": 1,
                    "page_size": 10,
                    "sort_by": "pub_time",
                    "sort_order": "desc",
                }
            ]
        }
    }


# 新闻项响应
class NewsItem(BaseModel):
    id: int
    title: str
    abstract: str = ""
    body: Optional[str] = None
    pub_time: Optional[datetime] = None
    request_url: Optional[str] = None
    language_id: Optional[int] = None
    created_at: Optional[datetime] = None  # 保持字段定义，但允许为空
    source: Optional[str] = None
    location: Optional[str] = None
    is_first_release: bool = False
    is_favorited: bool = False

    model_config = ConfigDict(from_attributes=True,
                              json_encoders={datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None})


# 搜索响应
class SearchResponse(BaseModel):
    data: List[NewsItem]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    query_time_ms: float
    model_config = ConfigDict(from_attributes=True)


# 分页列表响应（与 search 的列表部分对齐，无 query_time_ms）
class NewsListResponse(BaseModel):
    data: List[NewsItem]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    model_config = ConfigDict(from_attributes=True)


# ================== 认证配置 ==================
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24
PASSWORD_RESET_EXPIRE_MINUTES = int(os.getenv("PASSWORD_RESET_EXPIRE_MINUTES", "30"))
PASSWORD_MIN_LENGTH = int(os.getenv("PASSWORD_MIN_LENGTH", "8"))
AUTH_USER = os.getenv("ADMIN_USER", "admin")
AUTH_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
security = HTTPBearer(auto_error=False)


def create_access_token(user_id: int, username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": str(user_id), "username": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[Dict[str, Any]]:
    if not credentials or not credentials.credentials:
        return None
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        username = payload.get("username")
        if sub:
            return {"user_id": int(sub), "username": username}
    except Exception:
        pass
    return None


def get_current_user_required(
    user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
) -> Dict[str, Any]:
    if not user:
        raise HTTPException(status_code=401, detail="未登录或 token 无效")
    return user


# ================== 辅助函数 ==================

def parse_time_range(publish_time: Optional[str]) -> tuple:
    if not publish_time: return None, None
    now = datetime.now()
    ranges = {
        '近一天': timedelta(days=1),
        '近一周': timedelta(weeks=1),
        '近一月': timedelta(days=30),
        '近三月': timedelta(days=90),
        '近一年': timedelta(days=365),
    }
    if publish_time in ranges:
        start_time = now - ranges[publish_time]
        return start_time, now
    return None, None


def extract_source_from_url(url: str) -> str:
    if not url: return ""
    try:
        domain = urlparse(url).netloc
        domain = re.sub(r'^www\.', '', domain)
        parts = domain.split('.')
        if len(parts) >= 2: return parts[-2].capitalize()
        return domain
    except:
        return ""


def get_language_name(db: Session, language_id: Optional[int]) -> str:
    if language_id is None:
        return "未知"
    row = db.query(models.Language).filter(models.Language.id == language_id).first()
    return row.name if row and row.name else "未知"


def get_language_name_map(db: Session, language_ids: List[Optional[int]]) -> Dict[int, str]:
    ids = [x for x in language_ids if x is not None]
    if not ids:
        return {}
    rows = db.query(models.Language.id, models.Language.name).filter(models.Language.id.in_(ids)).all()
    return {int(r.id): (r.name or "未知") for r in rows}


def get_user_favorite_news_ids(
    db: Session,
    user_id: Optional[int],
    news_ids: List[int],
) -> set[int]:
    """按用户和新闻 ID 列表批量查询收藏状态。"""
    if not user_id or user_id <= 0 or not news_ids:
        return set()
    rows = (
        db.query(models.UserFavorite.news_id)
        .filter(
            models.UserFavorite.user_id == user_id,
            models.UserFavorite.news_id.in_(news_ids),
        )
        .all()
    )
    return {int(r.news_id) for r in rows}


def resolve_country_to_language(db: Session, country: Optional[str]) -> Optional[int]:
    if not country or not str(country).strip():
        return None
    name = str(country).strip()
    row = db.query(models.Language.id).filter(models.Language.name == name).first()
    return int(row.id) if row else None


def _columns_for_hit_location(hit_location: str):
    """按 hit_location 返回参与检索的列。标题=title，摘要=abstract，正文=body，全文=title+abstract+body。"""
    if hit_location == "标题":
        return [models.News.title]
    if hit_location == "摘要":
        return [models.News.abstract]
    if hit_location == "正文":
        return [models.News.body]
    # 全文：标题+摘要+正文
    return [models.News.title, models.News.abstract, models.News.body]


def _term_in_columns(columns: list, term: str):
    """单个词在给定列中任意一处包含即命中（OR）"""
    return or_(*[c.contains(term) for c in columns if c is not None])


def build_filter_conditions(
    search_params: SearchRequest,
    language_id: Optional[int],
) -> List[Any]:
    """
    构建筛选条件：keyword/topic 主检索；must_include 必须全部包含（AND）；
    any_include 不参与 WHERE，仅用于排序；need_exclude 任一词出现则排除。
    hit_location 统一控制检索范围：标题/摘要/正文/全文。
    """
    final_conditions = []
    loc = search_params.hit_location or "全文"
    columns = _columns_for_hit_location(loc)

    # 1. 主检索：keyword 或 topic 至少命中一处（OR  across columns）
    keyword = (search_params.keyword or search_params.topic or "").strip()
    if keyword:
        final_conditions.append(_term_in_columns(columns, keyword))

    # 2. must_include：每个词都必须出现（AND）
    if search_params.must_include:
        for k in search_params.must_include.split():
            k = k.strip()
            if k:
                final_conditions.append(_term_in_columns(columns, k))

    # 3. need_exclude：任一词在范围内出现则排除（AND NOT 每个词）
    if search_params.need_exclude:
        for k in search_params.need_exclude.split():
            k = k.strip()
            if k:
                final_conditions.append(not_(_term_in_columns(columns, k)))

    # 4. 时间
    start_dt, end_dt = None, None
    if search_params.publish_time:
        start_dt, end_dt = parse_time_range(search_params.publish_time)
    if search_params.start_time:
        try:
            start_dt = datetime.fromisoformat(search_params.start_time)
        except Exception:
            pass
    if search_params.end_time:
        try:
            end_dt = datetime.fromisoformat(search_params.end_time)
        except Exception:
            pass
    if start_dt:
        final_conditions.append(models.News.pub_time >= start_dt)
    if end_dt:
        final_conditions.append(models.News.pub_time <= end_dt)

    # 5. 数据源
    if search_params.data_source:
        final_conditions.append(models.News.request_url.contains(search_params.data_source))

    # 6. 国家/语言（标准列 news.language_id）
    if language_id is not None:
        final_conditions.append(models.News.language_id == language_id)

    return final_conditions


def build_any_include_order_expression(search_params: SearchRequest):
    """
    构建「是否命中 any_include」的表达式，用于 ORDER BY 优先展示命中结果。
    未传 any_include 时返回 None。
    """
    if not search_params.any_include:
        return None
    loc = search_params.hit_location or "全文"
    columns = _columns_for_hit_location(loc)
    terms = [k.strip() for k in search_params.any_include.split() if k.strip()]
    if not terms:
        return None
    conds = [_term_in_columns(columns, t) for t in terms]
    return or_(*conds)


# 通用分页查询函数
def get_paginated_field(db: Session, field, page: int, size: int):
    offset = (page - 1) * size
    query = db.query(models.News.id, field.label('value'))
    total = db.query(func.count(models.News.id)).scalar()
    items = query.order_by(desc(models.News.id)).offset(offset).limit(size).all()

    formatted = []
    for item in items:
        val = item.value
        if isinstance(val, datetime): val = val.strftime('%Y-%m-%d %H:%M:%S')
        formatted.append({"id": item.id, "value": str(val) if val else "—"})

    return {
        "data": formatted,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size,
        "has_next": page * size < total,
        "has_prev": page > 1
    }


# ===================================================================
# API 路由定义
# ===================================================================

@app.get("/", tags=["根目录"])
async def root():
    return {"status": "success", "message": "News API is running"}


# 【接口1】GET /api/dashboard/stats
@app.get("/api/dashboard/stats", response_model=StatsResponse, tags=["仪表盘"])
def get_stats(db: Session = Depends(get_db)):
    try:
        total_news = db.query(func.count(models.News.id)).scalar()
        lang_counts = db.query(
            models.News.language_id,
            func.count(models.News.id).label('count')
        ).group_by(models.News.language_id).all()

        language_stats = []
        for language_value, count in lang_counts:
            language_stats.append({
                "id": language_value or "未知",
                "count": count,
                "name": get_language_name(db, language_value)
            })

        total_languages = len(language_stats)

        return {
            "total_news": total_news,
            "total_languages": total_languages,
            "language_stats": language_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计查询失败: {str(e)}")


# 【接口2】GET /api/dashboard/news 分页列表（替代 titles/abstracts/pub-times/request-urls 四接口）
@app.get("/api/dashboard/news", response_model=NewsListResponse, tags=["仪表盘"])
def get_news_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    sort_by: Optional[str] = Query("pub_time"),
    sort_order: Optional[str] = Query("desc"),
    user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """分页获取新闻列表，与 POST /search 的列表字段一致，不含 body 可减体积。"""
    try:
        query = db.query(models.News)
        total = query.with_entities(func.count(models.News.id)).scalar()
        sort_field = getattr(models.News, sort_by or "pub_time", models.News.pub_time)
        order_direction = desc(sort_field) if (sort_order or "desc") == "desc" else sort_field.asc()
        query = query.order_by(order_direction)
        query = query.with_entities(
            models.News.id,
            models.News.title,
            models.News.abstract,
            models.News.body,
            models.News.pub_time,
            models.News.request_url,
            models.News.language_id,
        )
        results = query.offset((page - 1) * size).limit(size).all()
        language_ids = list({row.language_id for row in results if row.language_id is not None})
        lang_name_map = get_language_name_map(db, language_ids)
        user_id = int(user["user_id"]) if user and user.get("user_id") else 0
        favorite_ids = get_user_favorite_news_ids(db, user_id, [row.id for row in results])
        data_list = []
        for row in results:
            data_list.append(
                NewsItem(
                    id=row.id,
                    title=row.title or "无标题",
                    abstract=row.abstract or (row.body[:200] + "..." if row.body else ""),
                    body=row.body,
                    pub_time=row.pub_time,
                    request_url=row.request_url,
                    language_id=row.language_id,
                    created_at=None,
                    source=extract_source_from_url(row.request_url),
                    location=lang_name_map.get(row.language_id, "未知"),
                    is_first_release=False,
                    is_favorited=row.id in favorite_ids,
                )
            )
        total_pages = (total + size - 1) // size if size else 0
        return NewsListResponse(
            data=data_list,
            total=total,
            page=page,
            page_size=size,
            total_pages=total_pages,
            has_next=page * size < total,
            has_prev=page > 1,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"列表查询失败: {str(e)}")


# 【接口2b】GET /api/dashboard/news/{id} 单条新闻详情（含 body）
@app.get("/api/dashboard/news/{news_id}", response_model=NewsItem, tags=["仪表盘"])
def get_news_by_id(news_id: int, db: Session = Depends(get_db)):
    """根据 id 获取单条新闻详情，用于详情页展示。"""
    row = (
        db.query(
            models.News.id,
            models.News.title,
            models.News.abstract,
            models.News.body,
            models.News.pub_time,
            models.News.request_url,
            models.News.language_id,
        )
        .filter(models.News.id == news_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="新闻不存在")
    lang_name_map = get_language_name_map(db, [row.language_id] if row.language_id is not None else [])
    return NewsItem(
        id=row.id,
        title=row.title or "无标题",
        abstract=row.abstract or (row.body[:200] + "..." if row.body else ""),
        body=row.body,
        pub_time=row.pub_time,
        request_url=row.request_url,
        language_id=row.language_id,
        created_at=None,
        source=extract_source_from_url(row.request_url),
        location=lang_name_map.get(row.language_id, "未知"),
        is_first_release=False,
    )


# 【接口3】POST /api/dashboard/search
@app.post("/api/dashboard/search", response_model=SearchResponse, tags=["仪表盘"])
async def search_news(
    params: SearchRequest,
    user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    import time
    start_ts = time.time()
    try:
        language_id = resolve_country_to_language(db, params.language or params.country)
        query = db.query(models.News)
        filters = build_filter_conditions(params, language_id)
        if filters:
            query = query.filter(and_(*filters))
        total = query.with_entities(func.count(models.News.id)).scalar()
        sort_field = getattr(models.News, params.sort_by, models.News.pub_time)
        order_direction = desc(sort_field) if (params.sort_order or "desc") == "desc" else sort_field.asc()
        any_include_expr = build_any_include_order_expression(params)
        if any_include_expr is not None:
            query = query.order_by(case((any_include_expr, 1), else_=0).desc(), order_direction)
        else:
            query = query.order_by(order_direction)
        offset = (params.page - 1) * params.page_size
        # 修正：移除 models.News.created_at，因为数据库中没有这个字段
        query = query.with_entities(
            models.News.id,
            models.News.title,
            models.News.abstract,
            models.News.body,
            models.News.pub_time,
            models.News.request_url,
            models.News.language_id
        )
        results = query.offset(offset).limit(params.page_size).all()
        language_ids = list({row.language_id for row in results if row.language_id is not None})
        lang_name_map = get_language_name_map(db, language_ids)
        user_id = int(user["user_id"]) if user and user.get("user_id") else 0
        favorite_ids = get_user_favorite_news_ids(db, user_id, [row.id for row in results])
        data_list = []
        for row in results:
            data_list.append(NewsItem(
                id=row.id,
                title=row.title or "无标题",
                abstract=row.abstract or (row.body[:200] + "..." if row.body else ""),
                body=row.body,
                pub_time=row.pub_time,
                request_url=row.request_url,
                language_id=row.language_id,
                created_at=None,  # 手动设为None
                source=extract_source_from_url(row.request_url),
                location=lang_name_map.get(row.language_id, "未知"),
                is_first_release=False,
                is_favorited=row.id in favorite_ids,
            ))
        query_time = (time.time() - start_ts) * 1000
        return SearchResponse(
            data=data_list, total=total, page=params.page, page_size=params.page_size,
            total_pages=(total + params.page_size - 1) // params.page_size if params.page_size else 0,
            has_next=params.page * params.page_size < total, has_prev=params.page > 1,
            query_time_ms=query_time
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="数据库查询失败")
# 【接口4】GET /api/dashboard/titles（已废弃，请用 GET /api/dashboard/news）
@app.get("/api/dashboard/titles", response_model=PaginatedFieldResponse, tags=["仪表盘"])
def get_titles(page: int = Query(1), size: int = Query(100), db: Session = Depends(get_db)):
    return get_paginated_field(db, models.News.title, page, size)


# 【接口5】GET /api/dashboard/abstracts（已废弃，请用 GET /api/dashboard/news）
@app.get("/api/dashboard/abstracts", response_model=PaginatedFieldResponse, tags=["仪表盘"])
def get_abstracts(page: int = Query(1), size: int = Query(100), db: Session = Depends(get_db)):
    return get_paginated_field(db, models.News.abstract, page, size)


# 【接口6】GET /api/dashboard/pub-times（已废弃，请用 GET /api/dashboard/news）
@app.get("/api/dashboard/pub-times", response_model=PaginatedFieldResponse, tags=["仪表盘"])
def get_pub_times(page: int = Query(1), size: int = Query(100), db: Session = Depends(get_db)):
    return get_paginated_field(db, models.News.pub_time, page, size)


# 【接口7】GET /api/dashboard/request-urls（已废弃，请用 GET /api/dashboard/news）
@app.get("/api/dashboard/request-urls", response_model=PaginatedFieldResponse, tags=["仪表盘"])
def get_request_urls(page: int = Query(1), size: int = Query(100), db: Session = Depends(get_db)):
    return get_paginated_field(db, models.News.request_url, page, size)


# ================== 仪表盘聚合接口（供 data-statistics 使用） ==================

@app.get("/api/dashboard/news-rank", tags=["仪表盘"])
def get_news_rank(
    type: Optional[str] = Query("day"),
    db: Session = Depends(get_db),
):
    """新闻排行榜：按发布时间取最近 N 条，返回 title、hotValue、trend。"""
    try:
        limit = 10
        query = (
            db.query(models.News.id, models.News.title, models.News.pub_time)
            .order_by(desc(models.News.pub_time))
            .limit(limit * 3)
        )
        rows = query.all()
        out = []
        for i, row in enumerate(rows[:limit]):
            out.append({
                "title": row.title or "无标题",
                "hotValue": f"{(len(rows) - i) * 0.1:.1f}w",
                "trend": "up" if i % 2 == 0 else "down",
            })
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/language-ratio", tags=["仪表盘"])
def get_language_ratio(db: Session = Depends(get_db)):
    """多语言占比：基于 language_stats 计算各语言占比，总和 100。"""
    try:
        total_news = db.query(func.count(models.News.id)).scalar() or 0
        if total_news == 0:
            return []
        lang_counts = (
            db.query(models.News.language_id, func.count(models.News.id).label("cnt"))
            .group_by(models.News.language_id)
            .all()
        )
        total = sum(c for _, c in lang_counts)
        out = []
        for language_value, cnt in lang_counts:
            name = get_language_name(db, language_value)
            pct = round((cnt / total) * 100) if total else 0
            out.append({"name": name, "value": pct})
        remainder = 100 - sum(x["value"] for x in out)
        if out and remainder != 0:
            out[0]["value"] = out[0]["value"] + remainder
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/media-source", tags=["仪表盘"])
def get_media_source(db: Session = Depends(get_db), limit: int = Query(7, le=20)):
    """主要媒体：从 request_url 解析域名并聚合，返回 name、score。"""
    try:
        rows = (
            db.query(models.News.request_url, func.count(models.News.id).label("cnt"))
            .filter(models.News.request_url.isnot(None), models.News.request_url != "")
            .group_by(models.News.request_url)
            .order_by(desc(func.count(models.News.id)))
            .limit(limit * 3)
            .all()
        )
        by_domain: Dict[str, int] = {}
        for url, cnt in rows:
            name = extract_source_from_url(url or "")
            if name:
                by_domain[name] = by_domain.get(name, 0) + cnt
        sorted_domains = sorted(by_domain.items(), key=lambda x: -x[1])[:limit]
        max_cnt = max((c for _, c in sorted_domains), default=1)
        return [{"name": n, "score": round(80 + (c / max_cnt) * 10, 1)} for n, c in sorted_domains]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/source-type", tags=["仪表盘"])
def get_source_type(db: Session = Depends(get_db)):
    """信源类型分布：按 request_url 是否含常见域名打标签，返回 name、value 占比。"""
    try:
        total_news = db.query(func.count(models.News.id)).scalar() or 0
        if total_news == 0:
            return [
                {"name": "官方媒体", "value": 32},
                {"name": "商业媒体", "value": 28},
                {"name": "独立媒体", "value": 12},
                {"name": "国际组织", "value": 15},
                {"name": "其他", "value": 13},
            ]
        official = (
            db.query(func.count(models.News.id))
            .filter(
                models.News.request_url.isnot(None),
                models.News.request_url != "",
                or_(
                    models.News.request_url.contains(".gov"),
                    models.News.request_url.contains("reuters"),
                    models.News.request_url.contains("xinhua"),
                ),
            )
            .scalar()
            or 0
        )
        other = total_news - official
        pct_official = round((official / total_news) * 100)
        pct_other = 100 - pct_official
        return [
            {"name": "官方/主流媒体", "value": pct_official},
            {"name": "其他", "value": pct_other},
        ]
    except Exception as e:
        return [
            {"name": "官方媒体", "value": 32},
            {"name": "商业媒体", "value": 28},
            {"name": "独立媒体", "value": 12},
            {"name": "国际组织", "value": 15},
            {"name": "其他", "value": 15},
        ]


# ================== 认证接口 ==================

class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    confirm_password: str
    full_name: str
    email: str
    phone: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


class UserProfileUpdateRequest(BaseModel):
    full_name: str
    email: str
    phone: str


class UserProfileResponse(BaseModel):
    id: int
    username: str
    full_name: str = ""
    email: str = ""
    phone: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


def _validate_password_rules(password: str, confirm_password: str):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="两次输入密码不一致")
    if len(password) < PASSWORD_MIN_LENGTH:
        raise HTTPException(status_code=400, detail=f"密码长度至少 {PASSWORD_MIN_LENGTH} 位")
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="密码需包含字母和数字")


def _hash_password(raw_password: str) -> str:
    return bcrypt.hash(raw_password)


def _is_bcrypt_hash(stored_password: str) -> bool:
    return stored_password.startswith("$2a$") or stored_password.startswith("$2b$") or stored_password.startswith("$2y$")


def verify_login_password(raw_password: str, stored_password: Optional[str]) -> tuple[bool, bool]:
    """返回 (是否通过, 是否需要升级为哈希)。"""
    if not stored_password:
        return False, False
    raw_password = str(raw_password or "")
    stored_password = str(stored_password or "")
    if _is_bcrypt_hash(stored_password):
        try:
            return bcrypt.verify(raw_password, stored_password), False
        except Exception:
            return False, False
    return raw_password == stored_password, True


def _serialize_user_profile(user_row: models.User) -> Dict[str, Any]:
    return {
        "id": int(user_row.id),
        "username": user_row.username,
        "full_name": user_row.full_name or "",
        "email": user_row.email or "",
        "phone": user_row.phone or "",
        "created_at": user_row.created_at,
        "updated_at": user_row.updated_at,
    }


def _build_password_reset_link(token: str) -> str:
    base = os.getenv("FRONTEND_RESET_PASSWORD_URL", "http://localhost:5173/reset-password")
    connector = "&" if "?" in base else "?"
    return f"{base}{connector}token={token}"


class BaseEmailSender:
    def send_password_reset(self, to_email: str, reset_link: str):
        raise NotImplementedError()


class LogEmailSender(BaseEmailSender):
    def send_password_reset(self, to_email: str, reset_link: str):
        print(f"[PasswordReset][LOG_ONLY] to={to_email}, reset_link={reset_link}")


class SMTPEmailSender(BaseEmailSender):
    def __init__(self):
        self.host = os.getenv("SMTP_HOST", "")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME", "")
        self.password = os.getenv("SMTP_PASSWORD", "")
        self.sender = os.getenv("SMTP_SENDER", self.username)
        self.use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    def send_password_reset(self, to_email: str, reset_link: str):
        msg = EmailMessage()
        msg["Subject"] = "密码重置"
        msg["From"] = self.sender
        msg["To"] = to_email
        msg.set_content(f"请访问以下链接重置密码（{PASSWORD_RESET_EXPIRE_MINUTES}分钟内有效）：\n{reset_link}")
        with smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls:
                server.starttls()
            if self.username:
                server.login(self.username, self.password)
            server.send_message(msg)


def get_email_sender() -> BaseEmailSender:
    enabled = os.getenv("SMTP_ENABLED", "false").lower() == "true"
    if enabled:
        return SMTPEmailSender()
    return LogEmailSender()


def get_user_for_login(db: Session, username: str, raw_password: str) -> Optional[Dict[str, Any]]:
    user_row = db.query(models.User).filter(models.User.username == username).first()
    if not user_row:
        return None
    is_valid, need_upgrade = verify_login_password(raw_password, user_row.password_hash)
    if not is_valid:
        return None
    if need_upgrade:
        user_row.password_hash = _hash_password(raw_password)
        user_row.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user_row)
    return _serialize_user_profile(user_row)


@app.post("/api/auth/login", tags=["认证"])
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """登录：优先数据库账号；兼容环境变量账号兜底。"""
    username = (body.username or "").strip()
    password = body.password or ""
    user_row = get_user_for_login(db, username, password)
    if user_row:
        token = create_access_token(user_row["id"], user_row["username"])
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user_row,
        }

    # 回退：兼容历史环境变量账号
    if username != AUTH_USER or password != AUTH_PASSWORD:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_access_token(0, username)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": 0,
            "username": username,
            "full_name": "",
            "email": "",
            "phone": "",
            "created_at": None,
            "updated_at": None,
        },
    }


@app.post("/api/auth/register", tags=["认证"])
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    username = (body.username or "").strip()
    full_name = (body.full_name or "").strip()
    email = (body.email or "").strip().lower()
    phone = (body.phone or "").strip()
    password = body.password or ""
    if not username or not full_name or not email or not phone:
        raise HTTPException(status_code=400, detail="注册字段不能为空")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise HTTPException(status_code=400, detail="邮箱格式不正确")
    if not re.match(r"^1[3-9]\d{9}$", phone):
        raise HTTPException(status_code=400, detail="手机号格式不正确")
    _validate_password_rules(password, body.confirm_password or "")

    if db.query(models.User.id).filter(models.User.username == username).first():
        raise HTTPException(status_code=409, detail="用户名已存在")
    if db.query(models.User.id).filter(models.User.email == email).first():
        raise HTTPException(status_code=409, detail="邮箱已存在")
    if db.query(models.User.id).filter(models.User.phone == phone).first():
        raise HTTPException(status_code=409, detail="手机号已存在")

    now = datetime.now(timezone.utc)
    row = models.User(
        username=username,
        password_hash=_hash_password(password),
        full_name=full_name,
        email=email,
        phone=phone,
        created_at=now,
        updated_at=now,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"user": _serialize_user_profile(row)}


@app.post("/api/auth/forgot-password", tags=["认证"])
def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    email = (body.email or "").strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="邮箱不能为空")

    user_row = db.query(models.User).filter(models.User.email == email).first()
    if user_row:
        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=PASSWORD_RESET_EXPIRE_MINUTES)
        token_row = models.PasswordResetToken(
            user_id=user_row.id,
            token_hash=token_hash,
            expires_at=expires_at,
            used_at=None,
            created_at=now,
        )
        db.add(token_row)
        db.commit()
        reset_link = _build_password_reset_link(raw_token)
        get_email_sender().send_password_reset(email, reset_link)
    # 防止邮箱枚举，统一返回成功文案
    return {"ok": True, "message": "若邮箱已注册，将收到密码重置链接"}


@app.post("/api/auth/reset-password", tags=["认证"])
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    token = (body.token or "").strip()
    if not token:
        raise HTTPException(status_code=400, detail="token 不能为空")
    _validate_password_rules(body.new_password or "", body.confirm_password or "")
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc)
    token_row = (
        db.query(models.PasswordResetToken)
        .filter(
            models.PasswordResetToken.token_hash == token_hash,
            models.PasswordResetToken.used_at.is_(None),
            models.PasswordResetToken.expires_at > now,
        )
        .order_by(desc(models.PasswordResetToken.id))
        .first()
    )
    if not token_row:
        raise HTTPException(status_code=400, detail="重置链接无效或已过期")
    user_row = db.query(models.User).filter(models.User.id == token_row.user_id).first()
    if not user_row:
        raise HTTPException(status_code=404, detail="用户不存在")
    user_row.password_hash = _hash_password(body.new_password)
    user_row.updated_at = now
    token_row.used_at = now
    db.commit()
    return {"ok": True}


@app.get("/api/auth/me", tags=["认证"])
def auth_me(
    user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """获取当前用户信息，需携带 Authorization: Bearer <token>。"""
    if not user:
        raise HTTPException(status_code=401, detail="未登录或 token 无效")
    user_id = int(user.get("user_id") or 0)
    if user_id <= 0:
        return {
            "id": 0,
            "username": user.get("username", ""),
            "full_name": "",
            "email": "",
            "phone": "",
            "created_at": None,
            "updated_at": None,
        }
    row = db.query(models.User).filter(models.User.id == user_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="用户不存在")
    return _serialize_user_profile(row)


@app.get("/api/user/profile", response_model=UserProfileResponse, tags=["用户"])
def get_user_profile(
    user: Dict[str, Any] = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    user_id = int(user.get("user_id") or 0)
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="当前账号不支持个人资料")
    row = db.query(models.User).filter(models.User.id == user_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="用户不存在")
    return _serialize_user_profile(row)


@app.put("/api/user/profile", response_model=UserProfileResponse, tags=["用户"])
def update_user_profile(
    body: UserProfileUpdateRequest,
    user: Dict[str, Any] = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    user_id = int(user.get("user_id") or 0)
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="当前账号不支持个人资料修改")
    full_name = (body.full_name or "").strip()
    email = (body.email or "").strip().lower()
    phone = (body.phone or "").strip()
    if not full_name or not email or not phone:
        raise HTTPException(status_code=400, detail="姓名、邮箱、手机号不能为空")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise HTTPException(status_code=400, detail="邮箱格式不正确")
    if not re.match(r"^1[3-9]\d{9}$", phone):
        raise HTTPException(status_code=400, detail="手机号格式不正确")

    row = db.query(models.User).filter(models.User.id == user_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="用户不存在")
    email_conflict = (
        db.query(models.User.id)
        .filter(models.User.email == email, models.User.id != user_id)
        .first()
    )
    if email_conflict:
        raise HTTPException(status_code=409, detail="邮箱已被占用")
    phone_conflict = (
        db.query(models.User.id)
        .filter(models.User.phone == phone, models.User.id != user_id)
        .first()
    )
    if phone_conflict:
        raise HTTPException(status_code=409, detail="手机号已被占用")

    row.full_name = full_name
    row.email = email
    row.phone = phone
    row.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(row)
    return _serialize_user_profile(row)


@app.post("/api/user/change-password", tags=["用户"])
def change_password(
    body: ChangePasswordRequest,
    user: Dict[str, Any] = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    user_id = int(user.get("user_id") or 0)
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="当前账号不支持修改密码")
    _validate_password_rules(body.new_password or "", body.confirm_password or "")
    row = db.query(models.User).filter(models.User.id == user_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="用户不存在")

    old_ok, need_upgrade = verify_login_password(body.old_password or "", row.password_hash)
    if not old_ok:
        raise HTTPException(status_code=400, detail="旧密码错误")
    # 若旧密码仍是明文，顺带迁移；最终统一覆盖为新哈希。
    if need_upgrade:
        row.password_hash = _hash_password(body.old_password or "")
    row.password_hash = _hash_password(body.new_password or "")
    row.updated_at = datetime.now(timezone.utc)
    db.commit()
    return {"ok": True}


class SearchHistoryRequest(BaseModel):
    keyword: str


class FavoriteToggleRequest(BaseModel):
    news_id: int


@app.get("/api/user/search-history", tags=["用户"])
def get_user_search_history(
    limit: int = Query(50, ge=1, le=200),
    user: Dict[str, Any] = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    if int(user.get("user_id") or 0) <= 0:
        return {"data": []}
    rows = (
        db.query(models.UserSearchHistory)
        .filter(models.UserSearchHistory.user_id == user["user_id"])
        .order_by(desc(models.UserSearchHistory.id))
        .limit(limit)
        .all()
    )
    return {
        "data": [
            {
                "id": r.id,
                "query": r.keyword,
                "time": (r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else ""),
            }
            for r in rows
        ]
    }


@app.post("/api/user/search-history", tags=["用户"])
def add_user_search_history(
    body: SearchHistoryRequest,
    user: Dict[str, Any] = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    if int(user.get("user_id") or 0) <= 0:
        return {"ok": False, "message": "当前账号未绑定用户表，无法保存搜索记录"}
    kw = (body.keyword or "").strip()
    if not kw:
        raise HTTPException(status_code=400, detail="keyword 不能为空")
    row = models.UserSearchHistory(
        user_id=user["user_id"],
        keyword=kw[:255],
        created_at=datetime.now(timezone.utc),
    )
    db.add(row)
    db.commit()
    return {"ok": True}


@app.get("/api/user/favorites", tags=["用户"])
def get_user_favorites(
    user: Dict[str, Any] = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    if int(user.get("user_id") or 0) <= 0:
        return {"news_ids": []}
    rows = (
        db.query(models.UserFavorite.news_id)
        .filter(models.UserFavorite.user_id == user["user_id"])
        .all()
    )
    return {"news_ids": [r.news_id for r in rows]}


@app.post("/api/user/favorites/toggle", tags=["用户"])
def toggle_user_favorite(
    body: FavoriteToggleRequest,
    user: Dict[str, Any] = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    if int(user.get("user_id") or 0) <= 0:
        return {"favorited": False, "message": "当前账号未绑定用户表，无法收藏"}
    news_id = body.news_id
    if not news_id:
        raise HTTPException(status_code=400, detail="news_id 不能为空")
    row = (
        db.query(models.UserFavorite)
        .filter(
            models.UserFavorite.user_id == user["user_id"],
            models.UserFavorite.news_id == news_id,
        )
        .first()
    )
    if row:
        db.delete(row)
        db.commit()
        return {"favorited": False}
    new_row = models.UserFavorite(
        user_id=user["user_id"],
        news_id=news_id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(new_row)
    db.commit()
    return {"favorited": True}


# ================== AI 分析接口（DeepSeek） ==================
class AIAnalyzeRequest(BaseModel):
    """请求体：待分析内容，支持纯文本或结构化描述。"""
    text: Optional[str] = Field(None, description="待分析的文本内容")
    data: Optional[Dict[str, Any]] = Field(None, description="可选的结构化数据，将转为简要描述后分析")


class AIAnalyzeResponse(BaseModel):
    analysis: str


def _resolve_ai_raw_content(body: AIAnalyzeRequest) -> str:
    raw_content = body.text
    if not raw_content and body.data is not None:
        raw_content = str(body.data)
    if not raw_content or not str(raw_content).strip():
        raise HTTPException(status_code=400, detail="请提供 text 或 data 内容")
    return str(raw_content).strip()


@app.post("/api/ai/analyze", response_model=AIAnalyzeResponse, tags=["AI"])
def ai_analyze(body: AIAnalyzeRequest):
    """
    接收一定格式的数据，调用 DeepSeek 接口返回简要分析结果。
    需配置环境变量 DEEPSEEK_API_KEY。
    """
    deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        raise HTTPException(
            status_code=503,
            detail="未配置 DEEPSEEK_API_KEY，无法使用 AI 分析服务",
        )
    raw_content = _resolve_ai_raw_content(body)
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=deepseek_api_key,
            base_url="https://api.deepseek.com",
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个有帮助的助手。请对用户提供的内容进行简要分析，输出简洁的结论与要点，控制在 300 字以内。",
                },
                {"role": "user", "content": raw_content[:8000]},
            ],
            stream=False,
        )
        analysis = (response.choices[0].message.content or "").strip()
        return AIAnalyzeResponse(analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI 服务调用失败: {str(e)}")


@app.post("/api/ai/analyze/stream", tags=["AI"])
def ai_analyze_stream(body: AIAnalyzeRequest):
    deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        raise HTTPException(status_code=503, detail="未配置 DEEPSEEK_API_KEY，无法使用 AI 分析服务")
    raw_content = _resolve_ai_raw_content(body)

    def gen():
        try:
            from openai import OpenAI
            client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个有帮助的助手。请对用户提供的内容进行简要分析，输出简洁的结论与要点。",
                    },
                    {"role": "user", "content": raw_content[:8000]},
                ],
                stream=True,
            )
            for chunk in stream:
                delta = ""
                try:
                    if chunk and chunk.choices and chunk.choices[0].delta:
                        delta = chunk.choices[0].delta.content or ""
                except Exception:
                    delta = ""
                if delta:
                    yield f"data: {json.dumps({'delta': delta}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")


# ================== 启动入口 ==================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
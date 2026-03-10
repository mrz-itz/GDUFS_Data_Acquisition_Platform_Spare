# database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from urllib.parse import quote_plus

# PostgreSQL 配置（可由环境变量覆盖）
DB_HOST = os.getenv("DB_HOST", "192.168.207.171")
DB_PORT = os.getenv("DB_PORT", "54333")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "DG@admin")
DB_NAME = os.getenv("DB_NAME", "union_spider")

encoded_password = quote_plus(DB_PASSWORD)
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    # 延迟导入以避免循环依赖
    from models import News, Language, User, UserSearchHistory, UserFavorite, PasswordResetToken
    Base.metadata.create_all(bind=engine)
    # 兼容已有库：在不破坏现有表的前提下补齐新增字段/约束
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE IF EXISTS public.app_user ADD COLUMN IF NOT EXISTS full_name VARCHAR(128)"))
        conn.execute(text("ALTER TABLE IF EXISTS public.app_user ADD COLUMN IF NOT EXISTS email VARCHAR(255)"))
        conn.execute(text("ALTER TABLE IF EXISTS public.app_user ADD COLUMN IF NOT EXISTS phone VARCHAR(32)"))
        conn.execute(text("ALTER TABLE IF EXISTS public.app_user ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP"))
        conn.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_app_user_email ON public.app_user (email) "
                "WHERE email IS NOT NULL"
            )
        )
        conn.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_app_user_phone ON public.app_user (phone) "
                "WHERE phone IS NOT NULL"
            )
        )
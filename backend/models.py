# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from database import Base


class Language(Base):
    """语言表，通过 id 关联 news.language_id"""
    __tablename__ = "language"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))


class News(Base):
    __tablename__ = 'news'
    # __table_args__ = {'schema': 'dg_dev_crawler'}  # 如果使用特定schema
    # 注意：数据库表无 created_at 列，不要在此定义，否则查询会报 Unknown column

    id = Column(Integer, primary_key=True, index=True)
    request_url = Column(String(1000))
    title = Column(Text)
    abstract = Column(Text)
    body = Column(Text)
    pub_time = Column(DateTime)
    language_id = Column(Integer)


class User(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(128))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(32), unique=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class PasswordResetToken(Base):
    __tablename__ = "password_reset_token"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("app_user.id"), index=True, nullable=False)
    token_hash = Column(String(64), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False)


class UserSearchHistory(Base):
    __tablename__ = "user_search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("app_user.id"), index=True, nullable=False)
    keyword = Column(String(255), nullable=False)
    created_at = Column(DateTime)


class UserFavorite(Base):
    __tablename__ = "user_favorite"
    __table_args__ = (
        UniqueConstraint("user_id", "news_id", name="uq_user_news_favorite"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("app_user.id"), index=True, nullable=False)
    news_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime)
# -*- coding: utf-8 -*-
"""
数据库配置模块
使用 SQLAlchemy 连接 SQLite 数据库
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 数据库文件路径：backend/data/chat_history.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# 确保 data 目录存在
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'chat_history.db')}"

# 创建数据库引擎（SQLite 需要 check_same_thread=False 以支持多线程访问）
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # 生产环境设为 False，调试时可设为 True 查看 SQL 日志
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 ORM 基类
Base = declarative_base()


def get_db():
    """
    数据库会话依赖项
    用于 FastAPI 的 Depends() 注入，确保请求结束后自动关闭会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -*- coding: utf-8 -*-
"""
FastAPI 应用入口
配置 CORS、挂载路由、初始化数据库
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import conversations, messages, stats

# 创建所有数据库表（如果不存在则创建）
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用实例
app = FastAPI(
    title="AI对话记录管理器",
    description="一个用于管理 AI 对话记录的后端 API，支持对话和消息的增删改查、搜索和统计功能。",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI 文档地址
    redoc_url="/redoc",     # ReDoc 文档地址
)

# 配置 CORS（跨域资源共享），允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 生产环境应限制为具体域名
    allow_credentials=True,
    allow_methods=["*"],       # 允许所有 HTTP 方法
    allow_headers=["*"],       # 允许所有请求头
)

# 注册路由，统一使用 /api/v1 前缀
app.include_router(conversations.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")
app.include_router(stats.router, prefix="/api/v1")


@app.get("/", tags=["健康检查"])
def root():
    """根路径 - 服务健康检查"""
    return {
        "message": "AI对话记录管理器 API 已启动",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/v1/health", tags=["健康检查"])
def health_check():
    """API 健康检查端点"""
    return {"status": "ok"}

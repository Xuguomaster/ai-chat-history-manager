# -*- coding: utf-8 -*-
"""
FastAPI 应用入口
配置 CORS、挂载路由、初始化数据库
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import conversations, messages, stats, ai

# 创建所有数据库表（如果不存在则创建）
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用实例
app = FastAPI(
    title="AI对话记录管理器",
    description="一个用于管理 AI 对话记录的后端 API，支持对话和消息的增删改查、搜索和统计功能。已接入小米Mimo AI服务。",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置 CORS（跨域资源共享），允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由，统一使用 /api/v1 前缀
app.include_router(conversations.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")
app.include_router(stats.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")


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

# -*- coding: utf-8 -*-
"""
Pydantic 请求/响应模型
用于 API 的数据验证和序列化
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==================== 消息相关 Schema ====================

class MessageBase(BaseModel):
    """消息基础模型"""
    role: str = Field(..., description="角色：user / assistant / system")
    content: str = Field(..., description="消息内容")


class MessageCreate(MessageBase):
    """创建消息请求模型"""
    pass


class MessageUpdate(BaseModel):
    """更新消息请求模型"""
    role: Optional[str] = Field(None, description="角色：user / assistant / system")
    content: Optional[str] = Field(None, description="消息内容")


class MessageResponse(MessageBase):
    """消息响应模型"""
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== 对话相关 Schema ====================

class ConversationBase(BaseModel):
    """对话基础模型"""
    title: str = Field(..., description="对话标题", min_length=1, max_length=255)
    source: str = Field("unknown", description="对话来源（如 ChatGPT、Claude 等）")
    tags: Optional[str] = Field(None, description="标签，多个标签用逗号分隔")


class ConversationCreate(ConversationBase):
    """创建对话请求模型"""
    messages: Optional[List[MessageCreate]] = Field(None, description="创建对话时可选附带的消息列表")


class ConversationUpdate(BaseModel):
    """更新对话请求模型（所有字段可选）"""
    title: Optional[str] = Field(None, description="对话标题", min_length=1, max_length=255)
    source: Optional[str] = Field(None, description="对话来源")
    tags: Optional[str] = Field(None, description="标签")


class ConversationResponse(ConversationBase):
    """对话响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    """对话列表响应模型（不包含消息详情，提升查询效率）"""
    id: int
    title: str
    source: str
    tags: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True


# ==================== 统计相关 Schema ====================

class StatsResponse(BaseModel):
    """统计信息响应模型"""
    total_conversations: int = Field(0, description="对话总数")
    total_messages: int = Field(0, description="消息总数")
    source_stats: dict = Field(default_factory=dict, description="按来源统计的对话数量")


# ==================== 通用响应 Schema ====================

class ErrorResponse(BaseModel):
    """错误响应模型"""
    detail: str = Field(..., description="错误详情")


class SuccessResponse(BaseModel):
    """成功响应模型"""
    message: str = Field(..., description="成功消息")

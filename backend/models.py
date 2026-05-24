# -*- coding: utf-8 -*-
"""
数据模型模块
定义 Conversation（对话）和 Message（消息）的 ORM 模型
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Conversation(Base):
    """对话模型 - 存储对话的基本信息"""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="对话ID")
    title = Column(String(255), nullable=False, comment="对话标题")
    source = Column(String(50), nullable=False, default="unknown", comment="对话来源（如 ChatGPT、Claude 等）")
    tags = Column(String(500), nullable=True, comment="标签，多个标签用逗号分隔")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关联消息列表（一对多关系）
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation(id={self.id}, title='{self.title}', source='{self.source}')>"


class Message(Base):
    """消息模型 - 存储对话中的每条消息"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="消息ID")
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, comment="所属对话ID")
    role = Column(String(20), nullable=False, comment="角色（user/assistant/system）")
    content = Column(Text, nullable=False, comment="消息内容")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关联所属对话（多对一关系）
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', conversation_id={self.conversation_id})>"

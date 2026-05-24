# -*- coding: utf-8 -*-
"""
对话业务逻辑服务层
处理对话的增删改查、搜索等核心业务
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from fastapi import HTTPException

from models import Conversation, Message


def get_conversation_list(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    source: Optional[str] = None,
    tag: Optional[str] = None,
    keyword: Optional[str] = None,
) -> tuple[List[dict], int]:
    """
    获取对话列表（支持分页、筛选、搜索）

    参数:
        db: 数据库会话
        skip: 跳过记录数（分页偏移量）
        limit: 每页记录数
        source: 按来源筛选
        tag: 按标签筛选
        keyword: 关键词搜索（匹配标题）

    返回:
        (对话列表, 总数)
    """
    query = db.query(Conversation)

    # 按来源筛选
    if source:
        query = query.filter(Conversation.source == source)

    # 按标签筛选（模糊匹配，因为标签存储为逗号分隔字符串）
    if tag:
        query = query.filter(Conversation.tags.like(f"%{tag}%"))

    # 关键词搜索（匹配标题）
    if keyword:
        query = query.filter(Conversation.title.like(f"%{keyword}%"))

    # 获取总数
    total = query.count()

    # 按更新时间倒序排列，分页
    conversations = (
        query.order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # 构造返回结果（包含每个对话的消息数量）
    result = []
    for conv in conversations:
        msg_count = db.query(func.count(Message.id)).filter(Message.conversation_id == conv.id).scalar()
        result.append({
            "id": conv.id,
            "title": conv.title,
            "source": conv.source,
            "tags": conv.tags,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": msg_count,
        })

    return result, total


def get_conversation_by_id(db: Session, conversation_id: int) -> Conversation:
    """
    根据ID获取对话详情（包含所有消息）

    参数:
        db: 数据库会话
        conversation_id: 对话ID

    返回:
        Conversation 对象

    异常:
        HTTPException: 对话不存在时抛出 404
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail=f"对话 ID={conversation_id} 不存在")
    return conversation


def create_conversation(db: Session, title: str, source: str, tags: Optional[str] = None, messages: Optional[List[dict]] = None) -> Conversation:
    """
    创建新对话

    参数:
        db: 数据库会话
        title: 对话标题
        source: 对话来源
        tags: 标签
        messages: 可选的消息列表

    返回:
        创建的 Conversation 对象
    """
    conversation = Conversation(
        title=title,
        source=source,
        tags=tags,
    )
    db.add(conversation)
    db.flush()  # 先刷新以获取自增ID，用于关联消息

    # 如果传入了消息列表，一并创建
    if messages:
        for msg_data in messages:
            message = Message(
                conversation_id=conversation.id,
                role=msg_data["role"],
                content=msg_data["content"],
            )
            db.add(message)

    db.commit()
    db.refresh(conversation)
    return conversation


def update_conversation(db: Session, conversation_id: int, update_data: dict) -> Conversation:
    """
    更新对话信息

    参数:
        db: 数据库会话
        conversation_id: 对话ID
        update_data: 需要更新的字段字典

    返回:
        更新后的 Conversation 对象

    异常:
        HTTPException: 对话不存在时抛出 404
    """
    conversation = get_conversation_by_id(db, conversation_id)

    # 只更新传入的非 None 字段
    for field, value in update_data.items():
        if value is not None and hasattr(conversation, field):
            setattr(conversation, field, value)

    db.commit()
    db.refresh(conversation)
    return conversation


def delete_conversation(db: Session, conversation_id: int) -> dict:
    """
    删除对话（级联删除关联消息）

    参数:
        db: 数据库会话
        conversation_id: 对话ID

    返回:
        操作结果字典

    异常:
        HTTPException: 对话不存在时抛出 404
    """
    conversation = get_conversation_by_id(db, conversation_id)
    db.delete(conversation)
    db.commit()
    return {"message": f"对话 ID={conversation_id} 已成功删除"}


def search_conversations(db: Session, keyword: str, skip: int = 0, limit: int = 20) -> tuple[List[dict], int]:
    """
    全文搜索对话（匹配标题、标签、消息内容）

    参数:
        db: 数据库会话
        keyword: 搜索关键词
        skip: 跳过记录数
        limit: 每页记录数

    返回:
        (对话列表, 总数)
    """
    # 查找标题或标签中包含关键词的对话ID
    matching_conv_ids = set()

    # 在对话标题和标签中搜索
    conv_matches = db.query(Conversation.id).filter(
        or_(
            Conversation.title.like(f"%{keyword}%"),
            Conversation.tags.like(f"%{keyword}%"),
        )
    ).all()
    for row in conv_matches:
        matching_conv_ids.add(row.id)

    # 在消息内容中搜索，找到关联的对话ID
    msg_matches = db.query(Message.conversation_id).filter(
        Message.content.like(f"%{keyword}%")
    ).distinct().all()
    for row in msg_matches:
        matching_conv_ids.add(row.conversation_id)

    if not matching_conv_ids:
        return [], 0

    # 查询这些对话的完整信息
    total = len(matching_conv_ids)
    conversations = (
        db.query(Conversation)
        .filter(Conversation.id.in_(matching_conv_ids))
        .order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []
    for conv in conversations:
        msg_count = db.query(func.count(Message.id)).filter(Message.conversation_id == conv.id).scalar()
        result.append({
            "id": conv.id,
            "title": conv.title,
            "source": conv.source,
            "tags": conv.tags,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": msg_count,
        })

    return result, total

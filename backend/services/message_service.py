# -*- coding: utf-8 -*-
"""
消息业务逻辑服务层
处理消息的增删改查等核心业务
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Conversation, Message


def get_messages_by_conversation(
    db: Session,
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
) -> tuple[List[Message], int]:
    """
    获取指定对话下的消息列表

    参数:
        db: 数据库会话
        conversation_id: 对话ID
        skip: 跳过记录数
        limit: 每页记录数

    返回:
        (消息列表, 总数)

    异常:
        HTTPException: 对话不存在时抛出 404
    """
    # 先验证对话是否存在
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail=f"对话 ID={conversation_id} 不存在")

    query = db.query(Message).filter(Message.conversation_id == conversation_id)
    total = query.count()

    messages = (
        query.order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return messages, total


def get_message_by_id(db: Session, message_id: int) -> Message:
    """
    根据ID获取单条消息

    参数:
        db: 数据库会话
        message_id: 消息ID

    返回:
        Message 对象

    异常:
        HTTPException: 消息不存在时抛出 404
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail=f"消息 ID={message_id} 不存在")
    return message


def create_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
    """
    向指定对话添加一条新消息

    参数:
        db: 数据库会话
        conversation_id: 对话ID
        role: 角色（user/assistant/system）
        content: 消息内容

    返回:
        创建的 Message 对象

    异常:
        HTTPException: 对话不存在时抛出 404
    """
    # 验证对话是否存在
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail=f"对话 ID={conversation_id} 不存在")

    # 验证角色是否合法
    valid_roles = ["user", "assistant", "system"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"无效的角色 '{role}'，必须是以下之一：{', '.join(valid_roles)}"
        )

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    db.add(message)

    # 更新对话的 updated_at 时间
    from datetime import datetime
    conversation.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(message)
    return message


def update_message(db: Session, message_id: int, update_data: dict) -> Message:
    """
    更新消息内容

    参数:
        db: 数据库会话
        message_id: 消息ID
        update_data: 需要更新的字段字典

    返回:
        更新后的 Message 对象

    异常:
        HTTPException: 消息不存在时抛出 404
    """
    message = get_message_by_id(db, message_id)

    # 如果更新了角色，验证角色是否合法
    if "role" in update_data and update_data["role"] is not None:
        valid_roles = ["user", "assistant", "system"]
        if update_data["role"] not in valid_roles:
            raise HTTPException(
                status_code=400,
                detail=f"无效的角色 '{update_data['role']}'，必须是以下之一：{', '.join(valid_roles)}"
            )

    for field, value in update_data.items():
        if value is not None and hasattr(message, field):
            setattr(message, field, value)

    db.commit()
    db.refresh(message)
    return message


def delete_message(db: Session, message_id: int) -> dict:
    """
    删除消息

    参数:
        db: 数据库会话
        message_id: 消息ID

    返回:
        操作结果字典

    异常:
        HTTPException: 消息不存在时抛出 404
    """
    message = get_message_by_id(db, message_id)
    db.delete(message)
    db.commit()
    return {"message": f"消息 ID={message_id} 已成功删除"}


def batch_create_messages(db: Session, conversation_id: int, messages_data: List[dict]) -> List[Message]:
    """
    批量创建消息

    参数:
        db: 数据库会话
        conversation_id: 对话ID
        messages_data: 消息数据列表

    返回:
        创建的 Message 对象列表

    异常:
        HTTPException: 对话不存在时抛出 404
    """
    # 验证对话是否存在
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail=f"对话 ID={conversation_id} 不存在")

    valid_roles = ["user", "assistant", "system"]
    created_messages = []

    for msg_data in messages_data:
        # 验证角色
        if msg_data.get("role") not in valid_roles:
            raise HTTPException(
                status_code=400,
                detail=f"无效的角色 '{msg_data.get('role')}'，必须是以下之一：{', '.join(valid_roles)}"
            )

        message = Message(
            conversation_id=conversation_id,
            role=msg_data["role"],
            content=msg_data["content"],
        )
        db.add(message)
        created_messages.append(message)

    # 更新对话的 updated_at 时间
    from datetime import datetime
    conversation.updated_at = datetime.utcnow()

    db.commit()

    # 刷新所有消息以获取ID
    for msg in created_messages:
        db.refresh(msg)

    return created_messages

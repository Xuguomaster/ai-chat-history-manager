# -*- coding: utf-8 -*-
"""
统计路由模块
提供对话和消息的统计信息
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Conversation, Message
from schemas import StatsResponse

router = APIRouter(prefix="/stats", tags=["统计信息"])


@router.get("", response_model=StatsResponse, summary="获取统计数据")
def get_stats(db: Session = Depends(get_db)):
    """
    获取系统统计数据，包括：
    - 对话总数
    - 消息总数
    - 按来源统计的对话数量
    """
    try:
        # 对话总数
        total_conversations = db.query(func.count(Conversation.id)).scalar() or 0

        # 消息总数
        total_messages = db.query(func.count(Message.id)).scalar() or 0

        # 按来源统计对话数量
        source_results = (
            db.query(Conversation.source, func.count(Conversation.id))
            .group_by(Conversation.source)
            .all()
        )
        source_stats = {source: count for source, count in source_results}

        return StatsResponse(
            total_conversations=total_conversations,
            total_messages=total_messages,
            source_stats=source_stats,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败：{str(e)}")

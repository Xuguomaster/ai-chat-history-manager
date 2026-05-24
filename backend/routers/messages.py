# -*- coding: utf-8 -*-
"""
消息路由模块
提供消息的 CRUD 接口
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    MessageCreate,
    MessageUpdate,
    MessageResponse,
    SuccessResponse,
)
from services import message_service

router = APIRouter(prefix="/messages", tags=["消息管理"])


@router.get("/conversation/{conversation_id}", response_model=List[MessageResponse], summary="获取对话的消息列表")
def list_messages(
    conversation_id: int,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=500, description="每页记录数"),
    db: Session = Depends(get_db),
):
    """
    获取指定对话下的所有消息，按创建时间正序排列。
    """
    try:
        messages, total = message_service.get_messages_by_conversation(
            db=db,
            conversation_id=conversation_id,
            skip=skip,
            limit=limit,
        )
        return messages
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取消息列表失败：{str(e)}")


@router.get("/{message_id}", response_model=MessageResponse, summary="获取消息详情")
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
):
    """
    根据ID获取单条消息详情。
    """
    try:
        message = message_service.get_message_by_id(db, message_id)
        return message
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取消息详情失败：{str(e)}")


@router.post("/conversation/{conversation_id}", response_model=MessageResponse, status_code=201, summary="添加消息")
def create_message(
    conversation_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
):
    """
    向指定对话添加一条新消息。
    """
    try:
        message = message_service.create_message(
            db=db,
            conversation_id=conversation_id,
            role=data.role,
            content=data.content,
        )
        return message
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建消息失败：{str(e)}")


@router.post("/conversation/{conversation_id}/batch", response_model=List[MessageResponse], status_code=201, summary="批量添加消息")
def batch_create_messages(
    conversation_id: int,
    messages: List[MessageCreate],
    db: Session = Depends(get_db),
):
    """
    向指定对话批量添加消息。
    """
    try:
        messages_data = [msg.model_dump() for msg in messages]
        created = message_service.batch_create_messages(
            db=db,
            conversation_id=conversation_id,
            messages_data=messages_data,
        )
        return created
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量创建消息失败：{str(e)}")


@router.put("/{message_id}", response_model=MessageResponse, summary="更新消息")
def update_message(
    message_id: int,
    data: MessageUpdate,
    db: Session = Depends(get_db),
):
    """
    更新消息内容或角色。只更新传入的非空字段。
    """
    try:
        update_data = data.model_dump(exclude_unset=True)
        message = message_service.update_message(
            db=db,
            message_id=message_id,
            update_data=update_data,
        )
        return message
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新消息失败：{str(e)}")


@router.delete("/{message_id}", response_model=SuccessResponse, summary="删除消息")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
):
    """
    删除指定消息。
    """
    try:
        result = message_service.delete_message(db, message_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除消息失败：{str(e)}")

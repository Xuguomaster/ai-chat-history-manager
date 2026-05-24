# -*- coding: utf-8 -*-
"""
对话路由模块
提供对话的 CRUD 接口和搜索功能
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationListResponse,
    SuccessResponse,
)
from services import conversation_service

router = APIRouter(prefix="/conversations", tags=["对话管理"])


@router.get("", response_model=list[ConversationListResponse], summary="获取对话列表")
def list_conversations(
    skip: int = Query(0, ge=0, description="跳过记录数（分页偏移量）"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    source: Optional[str] = Query(None, description="按来源筛选（如 ChatGPT、Claude）"),
    tag: Optional[str] = Query(None, description="按标签筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索（匹配标题）"),
    db: Session = Depends(get_db),
):
    """
    获取对话列表，支持分页、按来源/标签筛选、关键词搜索。
    返回结果不包含消息详情，但包含每个对话的消息数量。
    """
    try:
        conversations, total = conversation_service.get_conversation_list(
            db=db,
            skip=skip,
            limit=limit,
            source=source,
            tag=tag,
            keyword=keyword,
        )
        return conversations
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取对话列表失败：{str(e)}")


@router.get("/search", response_model=list[ConversationListResponse], summary="全文搜索对话")
def search_conversations(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    db: Session = Depends(get_db),
):
    """
    全文搜索对话，匹配标题、标签和消息内容。
    """
    try:
        conversations, total = conversation_service.search_conversations(
            db=db,
            keyword=keyword,
            skip=skip,
            limit=limit,
        )
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败：{str(e)}")


@router.get("/{conversation_id}", response_model=ConversationResponse, summary="获取对话详情")
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    """
    根据ID获取对话详情，包含该对话下的所有消息。
    """
    try:
        conversation = conversation_service.get_conversation_by_id(db, conversation_id)
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取对话详情失败：{str(e)}")


@router.post("", response_model=ConversationResponse, status_code=201, summary="创建对话")
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
):
    """
    创建新对话。可在创建时附带消息列表。
    """
    try:
        messages_data = None
        if data.messages:
            messages_data = [msg.model_dump() for msg in data.messages]

        conversation = conversation_service.create_conversation(
            db=db,
            title=data.title,
            source=data.source,
            tags=data.tags,
            messages=messages_data,
        )
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建对话失败：{str(e)}")


@router.put("/{conversation_id}", response_model=ConversationResponse, summary="更新对话")
def update_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    db: Session = Depends(get_db),
):
    """
    更新对话信息（标题、来源、标签）。只更新传入的非空字段。
    """
    try:
        update_data = data.model_dump(exclude_unset=True)
        conversation = conversation_service.update_conversation(
            db=db,
            conversation_id=conversation_id,
            update_data=update_data,
        )
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新对话失败：{str(e)}")


@router.delete("/{conversation_id}", response_model=SuccessResponse, summary="删除对话")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    """
    删除对话及其所有关联消息。
    """
    try:
        result = conversation_service.delete_conversation(db, conversation_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除对话失败：{str(e)}")

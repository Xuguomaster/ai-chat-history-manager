# -*- coding: utf-8 -*-
"""
AI 路由模块
提供对话AI回复接口
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from services.ai_service import chat_completion


router = APIRouter(prefix="/ai", tags=["AI服务"])


class ChatRequest(BaseModel):
    messages: list[dict] = Field(..., description="消息列表")
    provider: str = Field(default="mimo", description="AI服务商: mimo / openai")
    model: Optional[str] = Field(default=None, description="模型名称")
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=2000, ge=1, le=16000)


class ChatResponse(BaseModel):
    reply: str
    provider: str
    model: str


@router.post("/chat", response_model=ChatResponse, summary="AI对话")
async def ai_chat(req: ChatRequest):
    """
    调用AI大模型进行对话。
    支持小米Mimo和OpenAI。
    """
    try:
        reply = await chat_completion(
            messages=req.messages,
            provider=req.provider,
            model=req.model,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
        return ChatResponse(
            reply=reply,
            provider=req.provider,
            model=req.model or "default"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")
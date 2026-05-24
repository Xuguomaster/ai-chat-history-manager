from dotenv import load_dotenv
import os
import pathlib

# 加载 .env 文件
load_dotenv(pathlib.Path(__file__).parent.parent / '.env')

# -*- coding: utf-8 -*-
"""
AI 服务层
调用小米Mimo等AI API，支持OpenAI兼容格式
"""

from typing import Optional
import httpx


# ---------- 配置 ----------
# 从环境变量读取 API Key（也可直接写在这里）
MIMO_API_KEY = os.getenv("MIMO_API_KEY", "your-api-key-here")
MIMO_BASE_URL = os.getenv("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")
MIMO_MODEL = os.getenv("MIMO_MODEL", "mimo-v2-flash")

# OpenAI 备用
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


async def chat_completion(
    messages: list[dict],
    provider: str = "mimo",          # "mimo" 或 "openai"
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2000,
) -> str:
    """
    调用AI大模型进行对话

    Args:
        messages: 消息列表 [{"role": "user", "content": "..."}]
        provider: 使用的AI服务商
        model: 模型名称（不传则用默认）
        temperature: 温度参数
        max_tokens: 最大token数

    Returns:
        AI回复文本
    """
    # 选择配置
    if provider == "mimo":
        api_key = MIMO_API_KEY
        base_url = MIMO_BASE_URL
        default_model = MIMO_MODEL
    else:
        api_key = OPENAI_API_KEY
        base_url = OPENAI_BASE_URL
        default_model = OPENAI_MODEL

    if api_key in ("", "your-api-key-here"):
        raise ValueError(f"请在环境变量中设置 {provider.upper()}_API_KEY")

    url = f"{base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model or default_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
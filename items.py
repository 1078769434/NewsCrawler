# -*- coding: utf-8 -*-
# Date:2025-01-23 10 13
from pydantic import BaseModel, Field
from typing import Optional


class NewsItem(BaseModel):
    url: str = Field(..., description="新闻链接")
    title: str = Field(..., description="新闻标题")
    description: Optional[str] = Field(None, description="新闻简介")
    author: Optional[str] = Field(None, description="新闻作者")
    publish_time: Optional[str] = Field(None, description="新闻发布时间")
    content: Optional[str] = Field(None, description="新闻内容")
    images: Optional[list] = Field(None, description="新闻图片")
    meta: Optional[dict] = Field(None, description="新闻元数据")

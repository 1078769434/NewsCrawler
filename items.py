# -*- coding: utf-8 -*-
# Date:2025-01-23 10 13
from pydantic import BaseModel, Field
from typing import List, Optional


class NewsItem(BaseModel):
    """
    新闻数据模型。
    """

    title: str = Field(..., description="新闻标题")
    url: str = Field(..., description="新闻链接")
    content: str = Field(..., description="新闻内容")
    author: Optional[str] = Field(default=None, description="新闻作者")
    keywords: Optional[str] = Field(default=None, description="新闻关键词")
    intro: Optional[str] = Field(default=None, description="新闻简介")
    create_time: Optional[str] = Field(default=None, description="新闻创建时间")
    media_name: Optional[str] = Field(default=None, description="新闻媒体名称")
    images: Optional[List] = Field(default=None, description="新闻图片列表")

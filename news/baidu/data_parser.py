# -*- coding: utf-8 -*-
# Date:2025-04-11 17 19
from typing import Any
from bs4 import BeautifulSoup

from items import NewsItem


class BaiDuNewsDataParser:
    @staticmethod
    def extract_html_from_callback(callback_str: str) -> list[dict[str, Any]]:
        soup = BeautifulSoup(callback_str, "html.parser")
        results = []
        # 找到所有新闻条目容器
        items = soup.find_all("div", class_="category-wrap_iQLoo horizontal_1eKyQ")
        for item in items:
            # 提取链接
            a_tag = item.find("a", class_="img-wrapper_29V76")
            url = a_tag["href"] if a_tag else None

            # 提取标题
            title_tag = item.find("div", class_="c-single-text-ellipsis")
            title = title_tag.text.strip() if title_tag else None

            # 提取描述（优先 large，其次 small）
            desc_tag = item.find(
                "div", class_="hot-desc_1m_jR large_nSuFU"
            ) or item.find("div", class_="hot-desc_1m_jR small_Uvkd3")
            description = desc_tag.text.strip() if desc_tag else None
            if title and url:
                results.append(
                    NewsItem(title=title, description=description, url=url).model_dump()
                )
        return results[:10]

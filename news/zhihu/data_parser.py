# -*- coding: utf-8 -*-
# Date:2025-04-14 14 44
from typing import List, Dict
from bs4 import BeautifulSoup


class ZhiHuNewsDataParser:
    @staticmethod
    def parse_hot_news_data(callback_str: str) -> List[Dict]:
        soup = BeautifulSoup(callback_str, "html.parser")
        results = []
        # 找到所有新闻条目容器
        items = soup.find_all("div", class_="HotItem-content")
        for item in items:
            # 提取链接
            a_tag = item.find("a")
            url = a_tag["href"] if a_tag else None

            # 提取标题
            title_tag = item.find("h2", class_="HotItem-title")
            title = title_tag.text.strip() if title_tag else None

            # 提取描述（优先 large，其次 small）
            desc_tag = item.find("p", class_="HotItem-excerpt")
            description = desc_tag.text.strip() if desc_tag else None
            if title and url:
                results.append({"title": title, "description": description, "url": url})
        return results

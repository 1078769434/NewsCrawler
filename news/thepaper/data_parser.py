# -*- coding: utf-8 -*-
# Date:2025-04-14 14 07
import json
from typing import List, Dict
from argon_log import logger


class ThePaperNewsDataParser:
    @staticmethod
    def parse_hot_news_data(json_data: str) -> List[Dict]:
        json_data = json.loads(json_data)
        news_list = json_data.get("data", {}).get("hotNews", [])
        if not isinstance(news_list, list):
            logger.warning("新闻数据格式异常，data 字段不是列表")
            return []

        # 解析每条新闻
        parsed_news = []
        for news in news_list:
            if not isinstance(news, dict):
                logger.warning("新闻数据格式异常，单条新闻不是字典")
                continue
            try:
                # 解析新闻数据
                parsed_news.append(
                    {
                        "title": news.get("name", ""),  # 新闻标题
                        "url": "https://www.thepaper.cn/newsDetail_forward_"
                        + news.get("contId", ""),
                    }
                )
            except Exception as e:
                logger.warning(f"解析单条新闻数据失败: {e}, 新闻数据: {news}")
                continue  # 跳过当前新闻，继续解析下一条
        return parsed_news

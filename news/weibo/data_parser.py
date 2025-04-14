# -*- coding: utf-8 -*-
# Date:2025-04-14 15 54
import json
from typing import List, Dict
from argon_log import logger


class WeiBoNewsDataParser:
    @staticmethod
    def parse_hot_news_data(json_data: str) -> List[Dict]:
        json_data = json.loads(json_data)
        try:
            news_list = (
                json_data.get("data", {}).get("cards", [])[0].get("card_group", [])
            )
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
                            "title": news.get("desc", ""),  # 新闻标题
                            "url": news.get("scheme", ""),
                        }
                    )
                except Exception as e:
                    logger.warning(f"解析单条新闻数据失败: {e}, 新闻数据: {news}")
                    continue  # 跳过当前新闻，继续解析下一条
            return parsed_news
        except (IndexError, AttributeError, TypeError) as e:
            logger.warning(f"获取 news_list 时发生异常: {e}")

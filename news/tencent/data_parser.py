from typing import List, Dict
from argon_log import logger
from items import NewsItem


# 腾讯新闻数据解析器
class TencentNewsDataParser:
    @staticmethod
    def parse_hot_news_data(json_data: Dict) -> List[Dict]:
        """
        解析新闻数据。

        :param json_data: 包含新闻数据的 JSON 字典
        :return: 包含新闻数据的列表，每个新闻是一个字典
        """
        try:
            # 提取新闻列表，如果 data 不存在则返回空列表
            news_list = json_data.get("data", [])
            if not isinstance(news_list, list):
                logger.warning("新闻数据格式异常，data 字段不是列表")
                return []

            # 解析每条新闻
            results = []
            for news in news_list:
                if not isinstance(news, dict):
                    logger.warning("新闻数据格式异常，单条新闻不是字典")
                    continue
                try:
                    results.append(
                        NewsItem(
                            title=news.get("title"),
                            url=news.get("link_info", {}).get("url"),
                            description=news.get("intro"),
                        ).model_dump()
                    )
                except Exception as e:
                    logger.warning(f"解析单条新闻数据失败: {e}, 新闻数据: {news}")
                    continue  # 跳过当前新闻，继续解析下一条

            return results
        except Exception as e:
            logger.error(f"解析新闻数据失败: {e}")
            return []  # 返回空列表表示解析失败

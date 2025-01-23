from typing import List, Dict
from argon_log import logger


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
            parsed_news = []
            for news in news_list:
                if not isinstance(news, dict):
                    logger.warning("新闻数据格式异常，单条新闻不是字典")
                    continue

                try:
                    # 解析新闻数据
                    parsed_news.append(
                        {
                            "id": news.get("id", ""),  # 新闻 ID
                            "title": news.get("title", ""),  # 新闻标题
                            "url": news.get("link_info", {}).get("url", "")
                            if news.get("link_info")
                            else "",  # 新闻链接
                            "content": news.get("content", ""),  # 新闻内容
                            "author": news.get("author", ""),  # 新闻作者
                            "intro": news.get("intro", ""),  # 新闻简介
                            "publish_time": news.get("publish_time", ""),  # 发布时间
                            "media_name": news.get("media_info", {}).get("chl_name", "")
                            if news.get("media_info")
                            else "",  # 媒体名称
                            "images": news.get("pic_info", {}).get("big_img", [])
                            if news.get("pic_info")
                            else [],
                            # 图片列表
                            "category": news.get("category", {}).get("cate1_name", "")
                            if news.get("category")
                            else "",
                            # 新闻分类
                            "source": news.get("media_info", {}).get("chl_name", "")
                            if news.get("media_info")
                            else "",
                            # 新闻来源
                        }
                    )
                except Exception as e:
                    logger.warning(f"解析单条新闻数据失败: {e}, 新闻数据: {news}")
                    continue  # 跳过当前新闻，继续解析下一条

            return parsed_news
        except Exception as e:
            logger.error(f"解析新闻数据失败: {e}")
            return []  # 返回空列表表示解析失败

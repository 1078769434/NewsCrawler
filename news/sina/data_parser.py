# -*- coding: utf-8 -*-
import re
import json
from typing import List, Dict
from argon_log import logger


class DataParser:
    # 提取国内最新新闻列表数据
    @staticmethod
    def extract_china_new_json_from_jsonp(jsonp_data: str) -> Dict:
        """
        从 JSONP 数据中提取 JSON 部分并解析为 Python 字典。

        :param jsonp_data: JSONP 格式的字符串数据
        :return: 解析后的 Python 字典
        """
        try:
            # 使用正则表达式提取 JSON 部分
            match = re.search(
                r"try\{feedCardJsonpCallback\((\{.*?\})\);\}catch\(e\)\{\};",
                jsonp_data,
                re.DOTALL,
            )
            if not match:
                raise ValueError("未找到有效的 JSON 数据")

            # 提取 JSON 字符串
            json_str = match.group(1)

            # 将 JSON 字符串解析为 Python 字典
            data = json.loads(json_str)
            return data
        except Exception as e:
            logger.error(f"解析 JSONP 数据失败: {e}")
            return None

    # 提取新浪的热点新闻列表数据
    @staticmethod
    def extract_china_hot_json_from_jsonp(jsonp_data: str) -> dict:
        """
        从 JSONP 数据中提取 JSON 部分并解析为 Python 字典。

        :param jsonp_data: JSONP 格式的字符串数据
        :return: 解析后的 Python 字典
        """
        try:
            # 使用正则表达式提取 `hotNewsData =` 后面的 JSON 部分
            match = re.search(
                r"var\s+hotNewsData\s*=\s*(\{.*?\});", jsonp_data, re.DOTALL
            )
            if not match:
                raise ValueError("未找到有效的 JSON 数据")

            # 提取 JSON 字符串
            json_str = match.group(1)

            # 将 JSON 字符串解析为 Python 字典
            data = json.loads(json_str)
            return data
        except Exception as e:
            logger.error(f"解析 JSONP 数据失败: {e}")
            return None

    @staticmethod
    def parse_hot_news_data(json_data: Dict) -> List[Dict]:
        """
        解析热点新闻数据。

        :param json_data: 解析后的 JSON 字典
        :return: 包含热点新闻数据的列表，每个新闻是一个字典
        """
        try:
            # 提取热点新闻列表
            hot_news_list = json_data["data"]

            # 解析每条热点新闻
            parsed_hot_news = []
            for news in hot_news_list:
                parsed_hot_news.append(
                    {
                        "id": news.get("id", ""),  # 新闻 ID
                        "title": news.get("title", ""),  # 新闻标题
                        "url": news.get("url", ""),  # 新闻链接
                        "media": news.get("media", ""),  # 媒体名称
                        "create_date": news.get("create_date", ""),  # 创建日期
                        "create_time": news.get("create_time", ""),  # 创建时间
                        "top_num": news.get("top_num", ""),  # 热度值
                    }
                )

            return parsed_hot_news
        except Exception as e:
            logger.error(f"解析热点新闻数据失败: {e}")
            return []

    @staticmethod
    def parse_news_data(json_data: Dict) -> List[Dict]:
        """
        解析普通新闻数据。

        :param json_data: 解析后的 JSON 字典
        :return: 包含新闻数据的列表，每个新闻是一个字典
        """
        try:
            # 提取新闻列表
            news_list = json_data["result"]["data"]

            # 解析每条新闻
            parsed_news = []
            for news in news_list:
                parsed_news.append(
                    {
                        "title": news.get("title", ""),  # 新闻标题
                        "url": news.get("url", ""),  # 新闻链接
                        "wapurl": news.get("wapurl", ""),  # 移动端链接
                        "intro": news.get("intro", ""),  # 新闻简介
                        "ctime": news.get("ctime", ""),  # 创建时间
                        "media_name": news.get("media_name", ""),  # 媒体名称
                        "images": news.get("images", []),  # 图片列表
                    }
                )

            return parsed_news
        except Exception as e:
            logger.error(f"解析新闻数据失败: {e}")
            return []

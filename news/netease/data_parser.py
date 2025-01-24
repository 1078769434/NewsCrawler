import json
import re
from typing import Dict, Optional, Any, List
from argon_log import logger
from bs4 import BeautifulSoup


# 腾讯新闻数据解析器
class TencentNewsDataParser:
    @staticmethod
    def extract_json_from_callback(callback_str: str) -> Optional[Dict[str, Any]]:
        """
        从 data_callback() 的响应中提取 JSON 数据。

        :param callback_str: data_callback() 的响应字符串
        :return: 提取的 JSON 数据（字典形式），如果提取失败则返回 None
        """
        # 使用正则表达式匹配 data_callback() 包裹的 JSON 数据
        json_pattern = (
            r"data_callback\(\s*(.*?)\s*\)"  # 匹配 data_callback() 包裹的 JSON
        )
        match = re.search(
            json_pattern, callback_str, re.DOTALL
        )  # re.DOTALL 允许跨行匹配

        if match:
            try:
                # 提取匹配的 JSON 字符串并解析为字典
                json_str = match.group(1)
                json_data = json.loads(json_str)
                return json_data
            except json.JSONDecodeError as e:
                logger.error(f"JSON 解析失败: {e}")
                return None
        else:
            logger.error("未找到有效的 JSON 数据")
            return None

    @staticmethod
    def parse_hot_news_data(html_content: str) -> List[Dict]:
        soup = BeautifulSoup(html_content, "html.parser")
        recommendations = []

        # 找到class为"mt15 mod_jrtj"的div标签
        div = soup.find("div", class_="mt15 mod_jrtj")
        if div:
            # 找到div下的所有<li>标签
            for li in div.find_all("li"):
                a_tag = li.find("a")
                if a_tag:
                    title = a_tag.get("title")
                    href = a_tag.get("href")
                    if title and href:
                        recommendations.append({"title": title, "docurl": href})

        return recommendations

import json
import re
from typing import Dict, Optional, Any
from argon_log import logger


# CCTV新闻数据解析器
class CCTVNewsDataParser:
    @staticmethod
    def extract_json_from_china(callback_str: str) -> Optional[Dict[str, Any]]:
        """
        从 data_callback() 的响应中提取 JSON 数据。

        :param callback_str: china() 的响应字符串
        :return: 提取的 JSON 数据（字典形式），如果提取失败则返回 None
        """
        # 使用正则表达式匹配 china() 包裹的 JSON 数据
        json_pattern = r"china\(\s*(.*?)\s*\)"  # 匹配 china() 包裹的 JSON
        match = re.search(
            json_pattern, callback_str, re.DOTALL
        )  # re.DOTALL 允许跨行匹配

        if match:
            try:
                # 提取匹配的 JSON 字符串并解析为字典
                json_str = match.group(1)
                json_data = json.loads(json_str)
                return json_data["data"]["list"]
            except json.JSONDecodeError as e:
                logger.error(f"JSON 解析失败: {e}")
                return None
        else:
            logger.error("未找到有效的 JSON 数据")
            return None

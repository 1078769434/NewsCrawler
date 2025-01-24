import json
from typing import Optional, Any, List, Dict
from argon_log import logger


# 今日头条新闻数据解析器
class ToutiaoNewsDataParser:
    @staticmethod
    def extract_json_from_hot_news(json_str: str) -> Optional[List[Dict[str, Any]]]:
        try:
            json_data = json.loads(json_str)
            return json_data["data"]
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}")
            return None

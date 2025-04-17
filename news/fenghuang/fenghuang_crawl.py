# -*- coding: utf-8 -*-
# Date:2025-04-17 10 00
from argon_log import logger

from base.base_spider import BaseSpider
from news.fenghuang.data_parser import FengHuangNewsDataParser
from news.fenghuang.request_handler import fenghuang_request_handler
from save.database_handler import DatabaseHandler


class FengHuangNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()  # 调用基类初始化
        self.request_handler = fenghuang_request_handler
        self.data_parser = FengHuangNewsDataParser()
        self.database_handler = DatabaseHandler()
        self.latest_china_news_url = ""
        self.hot_news_url = "https://www.ifeng.com/"

    async def fetch_latest_china_news(self):
        logger.warning("暂不支持该新闻类型的抓取")

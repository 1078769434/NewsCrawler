# -*- coding: utf-8 -*-
# Date:2025-01-23 15 08
import asyncio
import json

from news.tencent.data_parser import TencentNewsDataParser
from news.tencent.request_handler import RequestHandler
from argon_log import logger
from parse.news_parse import get_news_content


class TencentNewsSpider:
    def __init__(self):
        self.request_handler = RequestHandler()
        self.data_parser = TencentNewsDataParser()
        # self.database_handler = DatabaseHandler()
        self.latest_china_news_url = ""
        self.hot_news_url = "https://i.news.qq.com/web_feed/getHotModuleList"

    async def fetch_hot_news(self):
        data = {
            "base_req": {"from": "pc"},
            "forward": "2",
            "qimei36": "0_FpZFnxfEm2k23",
            "device_id": "0_FpZFnxfEm2k23",
            "flush_num": 1,
            "channel_id": "news_news_top",
            "item_count": 20,
        }
        data = json.dumps(data, separators=(",", ":"))
        # 发送请求
        json_data = await self.request_handler.fetch_post_data(self.hot_news_url, data)
        if json_data:
            hot_news_data = self.data_parser.parse_hot_news_data(json_data)
            # 并发请求新闻页面的 HTML
            tasks = [self.process_news(news) for news in hot_news_data]
            await asyncio.gather(*tasks)

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        # 获取新闻页面的 HTML
        news_html = await self.request_handler.fetch_data(news["url"])
        if news_html:
            news_content = get_news_content(news_html)
            news_content["url"] = news["url"]
            logger.info(f"腾讯新闻:{news_content}")
            return news_content
        else:
            logger.error(f"获取新闻 HTML 失败: {news['url']}")


if __name__ == "__main__":
    spider = TencentNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())

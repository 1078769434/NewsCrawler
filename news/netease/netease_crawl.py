# -*- coding: utf-8 -*-
# Date:2025-01-23 16 57
import asyncio

from argon_log import logger
from base.base_spider import BaseSpider
from news.netease.request_handler import RequestHandler
from news.netease.data_parser import TencentNewsDataParser
from parse.news_parse import get_news_content
from save.database_handler import DatabaseHandler


class NeteaseNewsSpider(BaseSpider):
    def __init__(self):
        self.request_handler = RequestHandler()
        self.data_parser = TencentNewsDataParser()
        self.database_handler = DatabaseHandler()
        self.latest_china_news_url = "https://news.163.com/special/cm_guonei/"
        self.hot_news_url = "https://news.163.com/domestic/"

    async def fetch_hot_news(self):
        logger.info("开始抓取网易新闻-热门新闻...")
        response_text = await self.request_handler.fetch_data(self.hot_news_url)
        if response_text:
            # 解析数据
            json_data = self.data_parser.parse_hot_news_data(response_text)
            if json_data:
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in json_data]
                await asyncio.gather(*tasks)
        logger.info("网易新闻-热门新闻抓取完成。")

    async def fetch_latest_china_news(self):
        logger.info("开始抓取网易新闻-最新国内新闻...")
        response_text = await self.request_handler.fetch_data(
            self.latest_china_news_url
        )
        if response_text:
            # 解析数据
            json_data = self.data_parser.extract_json_from_callback(response_text)
            if json_data:
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in json_data]
                await asyncio.gather(*tasks)
        logger.info("网易新闻-最新国内新闻抓取完成。")

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        # 获取新闻页面的 HTML
        news_html = await self.request_handler.fetch_data(news["docurl"])
        if news_html:
            news_content = get_news_content(news_html)
            news_content["url"] = news["docurl"]
            logger.debug(f"网易新闻:{news_content}")
            return news_content
        else:
            logger.error(f"获取网易新闻 HTML 失败: {news['url']}")


if __name__ == "__main__":
    spider = NeteaseNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())

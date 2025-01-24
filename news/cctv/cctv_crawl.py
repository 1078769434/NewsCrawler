# -*- coding: utf-8 -*-
# Date:2025-01-24 09 59
import asyncio

from argon_log import logger
from base.base_spider import BaseSpider
from news.cctv.data_parser import CCTVNewsDataParser
from news.cctv.request_handler import cctv_request_handler
from parse.news_parse import get_news_content


class CCTVNewsSpider(BaseSpider):
    def __init__(self):
        self.request_handler = cctv_request_handler
        self.data_parser = CCTVNewsDataParser()
        self.latest_china_news_url = (
            "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp"
        )
        self.hot_news_url = ""

    async def fetch_hot_news(self):
        pass

    async def fetch_latest_china_news(self):
        logger.info("开始抓取CCTV新闻-最新国内新闻...")
        response_text = await self.request_handler.fetch_data_get(
            self.latest_china_news_url
        )
        if response_text:
            # 解析数据
            json_data = self.data_parser.extract_json_from_china(response_text)
            if json_data:
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in json_data]
                await asyncio.gather(*tasks)

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        # 获取新闻页面的 HTML
        news_html = await self.request_handler.fetch_data_get(news["url"])
        if news_html:
            news_content = get_news_content(news_html)
            news_content["url"] = news["url"]
            logger.info(f"CCTV新闻:{news_content}")
            return news_content
        else:
            logger.error(f"获取新闻 HTML 失败: {news['url']}")


if __name__ == "__main__":
    spider = CCTVNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_latest_china_news())

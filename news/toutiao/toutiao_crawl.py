# -*- coding: utf-8 -*-
# Date:2025-01-24 11 10
import asyncio

from argon_log import logger
from base.base_spider import BaseSpider
from news.toutiao.data_parser import ToutiaoNewsDataParser
from news.toutiao.request_handler import toutiao_request_handler
from parse.news_parse import get_news_content


class ToutiaoNewsSpider(BaseSpider):
    def __init__(self):
        self.request_handler = toutiao_request_handler
        self.data_parser = ToutiaoNewsDataParser()
        self.latest_china_news_url = ""
        self.hot_news_url = "https://www.toutiao.com/hot-event/hot-board/"

    async def fetch_hot_news(self):
        logger.info("正在获取今日头条热门新闻...")
        params = {
            "origin": "toutiao_pc",
            # "_signature": "_02B4Z6wo00f01zCjrTwAAIDD79TLJfBpgx8wh6mAAKvGlA8g8INgcfWNteRcVVCYirt6dvWO661iA3hGkslo4f2VNcGJyecAN3JBMqbKZnuO2Iwt6zNLi9cvCrJe-bpO1.oM4gAAEPUCmDk-16"
        }
        response_text = await self.request_handler.fetch_data_get(
            self.hot_news_url, params=params
        )
        if response_text:
            # 解析数据
            json_data = self.data_parser.extract_json_from_hot_news(response_text)
            if json_data:
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in json_data]
                await asyncio.gather(*tasks)

    async def fetch_latest_china_news(self):
        pass

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        # 获取新闻页面的 HTML
        news_html = await self.request_handler.fetch_data_get(news["Url"])
        if news_html:
            news_content = get_news_content(news_html)
            news_content["url"] = news["Url"]
            logger.info(f"今日头条新闻:{news_content}")
            return news_content
        else:
            logger.error(f"获取新闻 HTML 失败: {news['Url']}")


if __name__ == "__main__":
    spider = ToutiaoNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())

# -*- coding: utf-8 -*-
# Date:2025-01-23 16 57
import asyncio

from argon_log import logger
from base.base_spider import BaseSpider
from model.news import NewsCategory, Source
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
        """
        抓取网易新闻-热门新闻。
        """
        await self.fetch_and_process_news(
            url=self.hot_news_url,
            category=NewsCategory.HOT.value,
            source=Source.NETEASE.value,
            log_prefix="网易新闻-热门新闻",
            parse_method=self.data_parser.parse_hot_news_data,
        )

    async def fetch_latest_china_news(self):
        """
        抓取网易新闻-最新国内新闻。
        """
        await self.fetch_and_process_news(
            url=self.latest_china_news_url,
            category=NewsCategory.LATEST_CHINA.value,
            source=Source.NETEASE.value,
            log_prefix="网易新闻-最新国内新闻",
            parse_method=self.data_parser.extract_json_from_callback,
        )

    async def fetch_and_process_news(
        self,
        url: str,
        category: str,
        source: str,
        log_prefix: str,
        parse_method: callable,
    ):
        """
        抓取并处理新闻数据。

        :param url: 新闻数据的 URL
        :param category: 新闻分类
        :param source: 新闻来源
        :param log_prefix: 日志前缀
        :param parse_method: 解析数据的方法
        """
        logger.info(f"开始抓取{log_prefix}...")
        response_text = await self.request_handler.fetch_data(url)
        if response_text:
            # 解析数据
            json_data = parse_method(response_text)
            if json_data:
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in json_data]
                news_content = await asyncio.gather(*tasks)

                # 过滤掉空值（抓取失败的新闻）
                news_content = [news for news in news_content if news]

                # 批量插入或更新新闻数据到数据库
                await self.database_handler.insert_or_update_news(
                    news_content,
                    category=category,
                    source=source,
                )
                logger.info(f"成功抓取 {len(news_content)} 条{log_prefix}。")
        logger.info(f"{log_prefix}抓取完成。")

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
            return None  # 返回空值表示抓取失败


if __name__ == "__main__":
    spider = NeteaseNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())

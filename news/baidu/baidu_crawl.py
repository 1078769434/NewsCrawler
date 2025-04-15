# -*- coding: utf-8 -*-
# Date:2025-04-11 17 11
import asyncio

from argon_log import logger

from base.base_spider import BaseSpider
from model.news import NewsCategory, Source
from news.baidu.data_parser import BaiDuNewsDataParser
from news.baidu.request_handler import baidu_request_handler


class BaiduNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()  # 调用基类初始化
        self.request_handler = baidu_request_handler
        self.data_parser = BaiDuNewsDataParser()
        self.latest_china_news_url = "https://top.baidu.com/board"
        self.hot_news_url = ""

    async def fetch_latest_china_news(self):
        """
        抓取baidu新闻-最新国内新闻。
        """
        await self.fetch_and_process_news(
            url=self.latest_china_news_url,
            category=NewsCategory.LATEST_CHINA.value,
            source=Source.BAIDU.value,
            log_prefix="baidu新闻-最新国内新闻",
            parse_method=self.data_parser.extract_html_from_callback,
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
        response_text = await self.request_handler.fetch_data_get(
            url, params={"tab": "realtime"}
        )
        if response_text:
            # 解析数据
            news_content = parse_method(response_text)
            logger.info(f"{news_content}")
            # 保存新闻内容
            if self.storage_enabled:
                try:
                    filepath = self.storage_handler.save(
                        news_content, source_name=source
                    )
                    logger.info(f"{log_prefix} 已保存到文件: {filepath}")
                except Exception as e:
                    logger.error(f"{log_prefix} 保存新闻数据失败: {e}")
            # 发送整合后的新闻通知
            if self.feishu_talk_notifier.enabled:
                await self.feishu_talk_notifier.send_multi_news_card(news_content)
        logger.info(f"{log_prefix}抓取完成。")

    async def fetch_hot_news(self):
        pass

    async def process_news(self, news):
        pass


if __name__ == "__main__":
    spider = BaiduNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_latest_china_news())

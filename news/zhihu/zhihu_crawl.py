# -*- coding: utf-8 -*-
# Date:2025-04-14 14 44
import asyncio

from argon_log import logger

from base.base_spider import BaseSpider
from config import settings
from model.news import NewsCategory, Source
from news.zhihu.data_parser import ZhiHuNewsDataParser
from news.zhihu.request_handler import zhihu_request_handler
from service.feishu import FeishuNotifier


class ZhiHuNewsSpider(BaseSpider):
    def __init__(self):
        self.request_handler = zhihu_request_handler
        self.data_parser = ZhiHuNewsDataParser()
        self.latest_china_news_url = ""
        self.hot_news_url = "https://www.zhihu.com/hot"
        self.feishu_talk_notifier = FeishuNotifier(
            webhook_url=settings.feishutalk.webhook_url,  # 替换为你的钉钉 Webhook URL
            secret=settings.feishutalk.secret,
        )

    async def fetch_latest_china_news(self):
        pass

    async def fetch_hot_news(self):
        await self.fetch_and_process_news(
            url=self.hot_news_url,
            category=NewsCategory.HOT.value,
            source=Source.ZHIHU.value,
            log_prefix="知乎新闻-热点新闻",
            parse_method=self.data_parser.parse_hot_news_data,
        )

    async def fetch_and_process_news(
        self,
        url: str,
        category: str,
        source: str,
        log_prefix: str,
        parse_method: callable,
    ):
        pass
        logger.info(f"开始抓取{log_prefix}...")
        response_text = await self.request_handler.fetch_data_get(url)
        if response_text:
            # 解析数据
            news_content = parse_method(response_text)
            logger.info(f"{news_content}")
            # 发送整合后的新闻通知
            if self.feishu_talk_notifier.enabled:
                await self.feishu_talk_notifier.send_multi_news_card(news_content)
        logger.info(f"{log_prefix}抓取完成。")

    async def process_news(self, news):
        pass


if __name__ == "__main__":
    spider = ZhiHuNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())

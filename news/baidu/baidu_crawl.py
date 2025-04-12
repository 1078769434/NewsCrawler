# -*- coding: utf-8 -*-
# Date:2025-04-11 17 11
import asyncio

from argon_log import logger

from base.base_spider import BaseSpider
from config import settings
from model.news import NewsCategory, Source
from news.baidu.data_parser import BaiDuNewsDataParser
from news.baidu.request_handler import baidu_request_handler
from service.feishu import FeishuNotifier


class BaiduNewsSpider(BaseSpider):
    def __init__(self):
        self.request_handler = baidu_request_handler
        self.data_parser = BaiDuNewsDataParser()
        self.latest_china_news_url = "https://top.baidu.com/board"
        self.hot_news_url = ""
        self.feishu_talk_notifier = FeishuNotifier(
            webhook_url=settings.feishutalk.webhook_url,  # 替换为你的钉钉 Webhook URL
            secret=settings.feishutalk.secret,  # 替换为你的钉钉密钥
            enabled=settings.feishutalk.enabled,  # 是否开启钉钉通知
        )

    async def fetch_latest_china_news(self):
        """
        抓取CCTV新闻-最新国内新闻。
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
            # 发送整合后的新闻通知
            if self.feishu_talk_notifier.enabled:
                await self.feishu_talk_notifier.send_pro_news_card(news_content)
        logger.info(f"{log_prefix}抓取完成。")

    async def fetch_hot_news(self):
        pass

    async def process_news(self, news):
        pass


if __name__ == "__main__":
    spider = BaiduNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_latest_china_news())

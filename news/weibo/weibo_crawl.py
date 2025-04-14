# -*- coding: utf-8 -*-
# Date:2025-04-14 15 54
import asyncio

from argon_log import logger

from base.base_spider import BaseSpider
from config import settings
from model.news import NewsCategory, Source
from news.weibo.data_parser import WeiBoNewsDataParser
from news.weibo.request_handler import weibo_request_handler
from service.feishu import FeishuNotifier


class WeiBoNewsSpider(BaseSpider):
    def __init__(self):
        self.request_handler = weibo_request_handler
        self.data_parser = WeiBoNewsDataParser()
        self.latest_china_news_url = ""
        self.hot_news_url = "https://m.weibo.cn/api/container/getIndex"
        self.feishu_notifier = FeishuNotifier(
            webhook_url=settings.feishutalk.webhook_url,  # 替换为你的钉钉 Webhook URL
            secret=settings.feishutalk.secret,  # 替换为你的钉
        )

    async def fetch_latest_china_news(self):
        pass

    async def fetch_hot_news(self):
        await self.fetch_and_process_news(
            url=self.hot_news_url,
            category=NewsCategory.HOT.value,
            source=Source.WEIBO.value,
            log_prefix="微博-热搜榜",
            parse_method=self.data_parser.parse_hot_news_data,
        )

    async def process_news(self, news):
        pass

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
        params = {
            "containerid": "106003type=25&t=3&disable_hot=1&filter_type=realtimehot",
            "luicode": "20000061",
            "lfid": "5070140584495876",
        }
        response_text = await self.request_handler.fetch_data_get(url, params)
        if response_text:
            # 解析数据
            news_content = parse_method(response_text)
            logger.info(f"{news_content}")
            # 发送整合后的新闻通知
            if self.feishu_notifier.enabled:
                await self.feishu_notifier.send_multi_news_card(news_content)
        logger.info(f"{log_prefix}抓取完成。")


if __name__ == "__main__":
    spider = WeiBoNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())

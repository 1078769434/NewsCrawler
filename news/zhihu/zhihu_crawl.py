# -*- coding: utf-8 -*-
# Date:2025-04-14 14 44
import asyncio

from argon_log import logger

from base.base_spider import BaseSpider
from model.news import NewsCategory, Source
from news.zhihu.data_parser import ZhiHuNewsDataParser
from news.zhihu.request_handler import zhihu_request_handler


class ZhiHuNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()  # 调用基类初始化
        self.request_handler = zhihu_request_handler
        self.data_parser = ZhiHuNewsDataParser()
        self.latest_china_news_url = ""
        self.hot_news_url = "https://www.zhihu.com/hot"

    async def fetch_latest_china_news(self):
        logger.warning("暂不支持该新闻类型的抓取")

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
        logger.info(f"开始抓取{log_prefix}...")
        response = await self.request_handler.fetch_data_get(url)
        response_text = response.text
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

    async def process_news(self, news):
        pass


if __name__ == "__main__":
    spider = ZhiHuNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())

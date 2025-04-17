# -*- coding: utf-8 -*-
# Date:2025-01-23 15 08
import asyncio
import json

from base.base_spider import BaseSpider
from model.news import NewsCategory, Source
from news.tencent.data_parser import TencentNewsDataParser
from news.tencent.request_handler import RequestHandler
from argon_log import logger
from parse.news_parse import get_news_content


class TencentNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()  # 调用基类初始化
        self.request_handler = RequestHandler()
        self.data_parser = TencentNewsDataParser()
        self.latest_china_news_url = ""
        self.hot_news_url = "https://i.news.qq.com/web_feed/getHotModuleList"

    async def fetch_latest_china_news(self):
        logger.warning("暂不支持该新闻类型的抓取")

    async def fetch_hot_news(self):
        """
        抓取腾讯新闻热榜新闻。
        """

        await self.fetch_and_process_news(
            url=self.hot_news_url,
            category=NewsCategory.HOT.value,
            source=Source.TENCENT.value,
            log_prefix="腾讯新闻热榜新闻",
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
        """
        抓取并处理新闻数据。

        :param url: 新闻数据的 URL
        :param data: 请求数据
        :param category: 新闻分类
        :param source: 新闻来源
        :param log_prefix: 日志前缀
        :param parse_method: 解析数据的方法
        """
        logger.info(f"开始抓取{log_prefix}...")
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
        json_data = await self.request_handler.fetch_post_data(url, data)
        if json_data:
            # 解析数据
            news_data = parse_method(json_data)
            if news_data:
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in news_data]
                news_content = await asyncio.gather(*tasks)

                # 过滤掉空值（抓取失败的新闻）
                news_content = [news for news in news_content if news]
                if self.to_database:
                    # 批量插入或更新新闻数据到数据库
                    await self.database_handler.insert_or_update_news(
                        news_content,
                        category=category,
                        source=source,
                    )
                logger.info(f"成功抓取 {len(news_content)} 条{log_prefix}。")
                # 保存新闻内容
                if self.storage_enabled:
                    try:
                        filepath = self.storage_handler.save(
                            news_content, source_name=source
                        )
                        logger.info(f"{log_prefix} 已保存到文件: {filepath}")
                    except Exception as e:
                        logger.error(f"{log_prefix} 保存新闻数据失败: {e}")
                if self.feishu_talk_notifier.enabled:
                    await self.feishu_talk_notifier.send_combined_news_notification(
                        news_content, title=f"{log_prefix}汇总"
                    )
        logger.info(f"{log_prefix}抓取完成。")

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
            return None  # 返回空值表示抓取失败


if __name__ == "__main__":
    spider = TencentNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())

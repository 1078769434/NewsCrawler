# -*- coding: utf-8 -*-
from news.sina.request_handler import RequestHandler
from news.sina.data_parser import DataParser
import asyncio
from argon_log import logger
from parse.news_parse import get_news_content
from utils.spider_tools import generate_timestamp


class SinaNewsSpider:
    def __init__(self):
        self.request_handler = RequestHandler()
        self.data_parser = DataParser()
        self.latest_china_news_url = "https://feed.sina.com.cn/api/roll/get"
        self.hot_news_url = "https://top.news.sina.com.cn/ws/GetTopDataList.php"

    async def fetch_hot_news(self):
        """
        获取新浪新闻-热点新闻-列表并并发请求新闻页面的 HTML 内容。。
        """
        hot_news_params = {
            "callback": "jQuery11110820057572079484_1737595214093",
            "top_type": "day",
            "top_cat": "news_china_suda",
            "top_time": "20250122",  # 可以根据需要动态生成日期
            "top_show_num": "20",
            "top_order": "DESC",
            "short_title": "1",
            "js_var": "hotNewsData",
            "_": generate_timestamp(),
        }

        # 发送请求
        response_text = await self.request_handler.fetch_data(
            self.hot_news_url, hot_news_params
        )
        if response_text:
            # 解析数据
            json_data = self.data_parser.extract_china_hot_json_from_jsonp(
                response_text
            )
            if json_data:
                hot_news_data = self.data_parser.parse_hot_news_data(json_data)
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in hot_news_data]
                await asyncio.gather(*tasks)

    async def fetch_latest_china_news(self):
        """
        获取新浪新闻-国内最新新闻-列表并并发请求新闻页面的 HTML 内容。
        """
        # 发送请求
        params = {
            "pageid": "121",
            "lid": "1356",
            "num": "20",
            "versionNumber": "1.2.4",
            "page": "1",
            "encode": "utf-8",
            "callback": "feedCardJsonpCallback",
            "_": generate_timestamp(),
        }
        response_text = await self.request_handler.fetch_data(
            self.latest_china_news_url, params
        )
        if response_text:
            # 解析数据
            json_data = self.data_parser.extract_china_new_json_from_jsonp(
                response_text
            )
            if json_data:
                news_data = self.data_parser.parse_news_data(json_data)
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in news_data]
                await asyncio.gather(*tasks)

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        # 获取新闻页面的 HTML
        news_html = await self.request_handler.fetch_data(news["url"])
        if news_html:
            news_content = get_news_content(news_html)
            logger.info(f"新浪新闻的列表页单条新闻:{news_content}")
        else:
            logger.error(f"获取新闻 HTML 失败: {news['url']}")


if __name__ == "__main__":
    spider = SinaNewsSpider()
    asyncio.run(spider.fetch_hot_news())

# -*- coding: utf-8 -*-
from base.base_spider import BaseSpider
from model.news import NewsCategory, Source
from news.sina.request_handler import sina_request_handler
from news.sina.data_parser import DataParser
import asyncio
from argon_log import logger
from parse.news_parse import get_news_content
from utils.spider_tools import generate_timestamp
from save.database_handler import DatabaseHandler


class SinaNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()  # 调用基类初始化
        self.request_handler = sina_request_handler
        self.data_parser = DataParser()
        self.database_handler = DatabaseHandler()  # 初始化数据库操作模块
        self.latest_china_news_url = "https://feed.sina.com.cn/api/roll/get"
        self.hot_news_url = "https://top.news.sina.com.cn/ws/GetTopDataList.php"

    async def fetch_latest_china_news(self):
        """
        获取新浪新闻-国内最新新闻-列表并并发请求新闻页面的 HTML 内容。
        """
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
        await self.fetch_and_process_news(
            url=self.latest_china_news_url,
            params=params,
            category=NewsCategory.LATEST_CHINA.value,
            source=Source.SINA.value,
            log_prefix="新浪新闻-最新国内新闻",
            parse_method=self.data_parser.extract_china_new_json_from_jsonp,
            data_parser=self.data_parser.parse_news_data,
        )

    async def fetch_hot_news(self):
        """
        获取新浪新闻-热点新闻-列表并并发请求新闻页面的 HTML 内容。
        """
        await self.fetch_and_process_news(
            url=self.hot_news_url,
            category=NewsCategory.HOT.value,
            source=Source.SINA.value,
            log_prefix="新浪新闻-热点新闻",
            parse_method=self.data_parser.extract_china_hot_json_from_jsonp,
            data_parser=self.data_parser.parse_hot_news_data,
        )

    async def fetch_and_process_news(
        self,
        url: str,
        category: str,
        source: str,
        log_prefix: str,
        parse_method: callable,
        data_parser: callable,
    ):
        """
        抓取并处理新闻数据。

        :param url: 新闻数据的 URL
        :param params: 请求参数
        :param category: 新闻分类
        :param source: 新闻来源
        :param log_prefix: 日志前缀
        :param parse_method: 解析 JSONP 数据的方法
        :param data_parser: 解析新闻数据的方法
        """
        logger.info(f"开始抓取{log_prefix}...")
        params = {
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
        response = await self.request_handler.fetch_data(url, params)
        response_text = response.text
        if response_text:
            # 解析 JSONP 数据
            json_data = parse_method(response_text)
            if json_data:
                # 解析新闻数据
                news_data = data_parser(json_data)
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
                # 保存新闻内容
                if self.storage_enabled:
                    try:
                        filepath = self.storage_handler.save(
                            news_content, source_name=source
                        )
                        logger.info(f"{log_prefix} 已保存到文件: {filepath}")
                    except Exception as e:
                        logger.error(f"{log_prefix} 保存新闻数据失败: {e}")

                logger.info(f"成功抓取 {len(news_content)} 条{log_prefix}。")
        logger.info(f"{log_prefix}抓取完成。")

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        # 获取新闻页面的 HTML
        response = await self.request_handler.fetch_data(news["url"])
        news_html = response.text
        if news_html:
            news_content = get_news_content(news_html)
            news_content["url"] = news["url"]
            logger.info(f"新浪新闻:{news_content}")
            return news_content
        else:
            logger.error(f"获取新闻 HTML 失败: {news['url']}")
            return None  # 返回空值表示抓取失败


if __name__ == "__main__":
    spider = SinaNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_latest_china_news())

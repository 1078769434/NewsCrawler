# -*- coding: utf-8 -*-
# Date:2025-01-24 11 10
import asyncio
import json

from argon_log import logger
from base.base_spider import BaseSpider
from news.toutiao.data_parser import ToutiaoNewsDataParser
from news.toutiao.request_handler import toutiao_request_handler
from parse.news_parse import get_news_content
from save.database_handler import DatabaseHandler


class ToutiaoNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()  # 调用基类初始化
        self.request_handler = toutiao_request_handler
        self.data_parser = ToutiaoNewsDataParser()
        self.database_handler = DatabaseHandler()
        self.latest_china_news_url = ""
        self.hot_news_url = "https://www.toutiao.com/hot-event/hot-board/"

    async def fetch_latest_china_news(self):
        logger.warning("暂不支持该新闻类型的抓取")

    async def fetch_hot_news(self):
        """
        抓取今日头条-热门新闻。
        """

        await self.fetch_and_process_news(
            url=self.hot_news_url,
            category="hot",
            source="toutiao",
            log_prefix="今日头条-热门新闻",
            parse_method=self.data_parser.extract_json_from_hot_news,
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
        :param params: 请求参数
        :param category: 新闻分类
        :param source: 新闻来源
        :param log_prefix: 日志前缀
        :param parse_method: 解析数据的方法
        """
        logger.info(f"开始抓取{log_prefix}...")
        params = {
            "origin": "toutiao_pc",
            # "_signature": "_02B4Z6wo00f01zCjrTwAAIDD79TLJfBpgx8wh6mAAKvGlA8g8INgcfWNteRcVVCYirt6dvWO661iA3hGkslo4f2VNcGJyecAN3JBMqbKZnuO2Iwt6zNLi9cvCrJe-bpO1.oM4gAAEPUCmDk-16"
        }
        response = await self.request_handler.fetch_data_get(url, params=params)
        response_text = response.text
        cookies = await self.get_cookies()
        if response_text:
            # 解析数据
            json_data = parse_method(response_text)
            if json_data:
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news, cookies) for news in json_data]
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

    async def process_news(self, news, cookies):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        # 获取新闻页面的 HTML
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://www.toutiao.com/a6824014300391145991/",
            "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        }
        response = await self.request_handler.fetch_data_get(
            news["Url"], headers=headers, cookies=cookies
        )
        news_html = response.text
        # logger.debug(f"获取新闻 HTML 成功: {news_html}")
        if news_html:
            news_content = get_news_content(news_html)
            news_content["url"] = news["Url"]
            logger.debug(f"今日头条新闻:{news_content}")
            return news_content
        else:
            logger.error(f"获取新闻 HTML 失败: {news['Url']}")
            return None  # 返回空值表示抓取失败

    async def get_cookies(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Content-Type": "application/json",
        }
        url = "https://ttwid.bytedance.com/ttwid/union/register/"
        data = {
            "region": "cn",
            "aid": 1768,
            "needFid": False,
            "service": "www.ixigua.com",
            "migrate_info": {"ticket": "", "source": "node"},
            "cbUrlProtocol": "https",
            "union": True,
        }
        data = json.dumps(data, separators=(",", ":"))
        response = await self.request_handler.fetch_data_post(
            url, headers=headers, data=data
        )
        logger.info(f"获取 ttwid 请求响应: {response.text}")
        ttwid = self.extract_ttwid_from_headers(response.headers)
        logger.info(f"获取 ttwid 成功: {ttwid}")
        cookies = {
            "ttwid": ttwid,
        }
        return cookies

    def extract_ttwid_from_headers(self, headers):
        set_cookie_headers = headers.get_list("Set-Cookie")
        for cookie in set_cookie_headers:
            if cookie.startswith("ttwid="):
                return cookie.split("ttwid=")[1].split(";")[0]
        raise ValueError("未从响应头中获取到 ttwid")


if __name__ == "__main__":
    spider = ToutiaoNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())

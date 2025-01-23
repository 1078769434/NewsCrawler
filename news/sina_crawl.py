# -*- coding: utf-8 -*-
# Date:2025-01-23 09 32
import json
import re
import httpx
import asyncio
from argon_log import logger
from parse.news_parse import get_news_content
from utils.spider_tools import generate_timestamp


class SinaNewsSpider:
    def __init__(self):
        self.headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://news.sina.com.cn/china/",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        }
        self.cookies = {
            "rotatecount": "1",
            "UOR": "www.bing.com,news.sina.com.cn,",
            "SINAGLOBAL": "120.224.113.145_1737594794.479271",
            "Apache": "120.224.113.145_1737594794.479272",
            "SUB": "_2AkMQzRjcf8NxqwFRmfoWzG7ia4RxzwrEieKmkekHJRMyHRl-yD9kqmgotRB6O002MxSnB-7ZXhqOwccJh8YXwvcNFOqE",
            "SUBP": "0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFMSKeYDNiQlbyDJ1HuHHnd",
            "directAd_samsung": "true",
            "ULV": "1737594902732:2:2:2:120.224.113.145_1737594794.479272:1737594791231",
        }
        self.params = {
            "pageid": "121",
            "lid": "1356",
            "num": "20",
            "versionNumber": "1.2.4",
            "page": "1",
            "encode": "utf-8",
            "callback": "feedCardJsonpCallback",
            "_": generate_timestamp(),
        }
        self.url = "https://feed.sina.com.cn/api/roll/get"

    async def fetch_sina_news(self):
        """
        获取新浪新闻列表并并发请求新闻页面的 HTML 内容。
        """
        async with httpx.AsyncClient() as client:
            # 获取新闻列表
            response = await client.get(
                self.url, headers=self.headers, cookies=self.cookies, params=self.params
            )
            logger.debug(response.text)
            logger.debug(response)
            json_data = self.extract_json_from_jsonp(response.text)

            # 解析新闻数据
            if json_data:
                news_data = self.parse_news_data(json_data)
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in news_data]
                await asyncio.gather(*tasks)

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        logger.debug(f"新浪新闻的列表页单条新闻:{news}")
        # 获取新闻页面的 HTML
        news_html = await self.fetch_news_html(news["url"])
        if news_html:
            news_content = get_news_content(news_html)
            logger.info(f"单条新浪新闻内容: {news_content}")
        else:
            logger.error(f"获取新闻 HTML 失败: {news['url']}")

    def extract_json_from_jsonp(self, jsonp_data):
        """
        使用正则表达式从 JSONP 数据中提取 JSON 部分并解析为 Python 字典。

        :param jsonp_data: JSONP 格式的字符串数据
        :return: 解析后的 Python 字典
        """
        try:
            # 使用正则表达式提取 JSON 部分
            # 匹配 try{feedCardJsonpCallback({...});}catch(e){};
            match = re.search(
                r"try\{feedCardJsonpCallback\((\{.*?\})\);\}catch\(e\)\{\};",
                jsonp_data,
                re.DOTALL,
            )

            if not match:
                raise ValueError("未找到有效的 JSON 数据")

            # 提取 JSON 字符串
            json_str = match.group(1)

            # 将 JSON 字符串解析为 Python 字典
            data = json.loads(json_str)
            return data
        except Exception as e:
            logger.error(f"新浪新闻的jsonp解析失败: {e}")
            return None

    def parse_news_data(self, json_data):
        """
        解析 JSON 数据中的新闻信息。

        :param json_data: 解析后的 JSON 字典
        :return: 包含新闻数据的列表，每个新闻是一个字典
        """
        try:
            # 提取新闻列表
            news_list = json_data["result"]["data"]

            # 解析每条新闻
            parsed_news = []
            for news in news_list:
                parsed_news.append(
                    {
                        "title": news.get("title", ""),  # 新闻标题
                        "url": news.get("url", ""),  # 新闻链接
                        "wapurl": news.get("wapurl", ""),  # 移动端链接
                        "intro": news.get("intro", ""),  # 新闻简介
                        "ctime": news.get("ctime", ""),  # 创建时间
                        "media_name": news.get("media_name", ""),  # 媒体名称
                        "images": news.get("images", []),  # 图片列表
                    }
                )

            return parsed_news
        except Exception as e:
            logger.error(f"解析新浪新闻数据失败: {e}")
            return []

    async def fetch_news_html(self, url):
        """
        请求新闻 URL 并获取 HTML 内容。

        :param url: 新闻的 URL
        :return: HTML 文本（如果请求成功），否则返回 None
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()  # 检查请求是否成功
                return response.text
        except httpx.HTTPStatusError as e:
            logger.error(
                f"请求新闻页面失败，状态码: {e.response.status_code}, URL: {url}"
            )
        except Exception as e:
            logger.error(f"请求新闻页面时发生错误: {e}, URL: {url}")
        return None


if __name__ == "__main__":
    spider = SinaNewsSpider()
    asyncio.run(spider.fetch_sina_news())

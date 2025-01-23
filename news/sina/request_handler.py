# -*- coding: utf-8 -*-
import httpx
from argon_log import logger
from typing import Optional


class RequestHandler:
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

    async def fetch_data(self, url: str, params: dict = None) -> Optional[str]:
        """
        发送 HTTP 请求并返回响应内容。

        :param url: 请求的 URL
        :param params: 请求参数
        :return: 响应内容（字符串）
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    url, headers=self.headers, cookies=self.cookies, params=params
                )
                response.raise_for_status()  # 检查请求是否成功
                return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"请求失败，状态码: {e.response.status_code}, URL: {url}")
        except Exception as e:
            logger.error(f"请求时发生错误: {e}, URL: {url}")
        return None

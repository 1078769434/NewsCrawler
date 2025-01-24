# -*- coding: utf-8 -*-
import httpx
from argon_log import logger
from typing import Optional


class RequestHandler:
    async def fetch_data(self, url: str) -> Optional[str]:
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://news.163.com/domestic/",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        }
        """
        发送 HTTP 请求并返回响应内容。

        :param url: 请求的 URL
        :param params: 请求参数
        :return: 响应内容（字符串）
        """
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()  # 检查请求是否成功
                return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"请求失败，状态码: {e.response.status_code}, URL: {url}")
        except Exception as e:
            logger.error(f"请求时发生错误: {e}, URL: {url}")
        return None

# -*- coding: utf-8 -*-
import httpx
from argon_log import logger
from typing import Optional


class RequestHandler:
    def __init__(self):
        self.headers = {
            "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://news.cctv.com/china/?spm=C94212.P4YnMod9m2uD.EWZW7h07k3Vs.2",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
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
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()  # 检查请求是否成功
                return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"请求失败，状态码: {e.response.status_code}, URL: {url}")
        except Exception as e:
            logger.error(f"请求时发生错误: {e}, URL: {url}")
        return None

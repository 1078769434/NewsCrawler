# -*- coding: utf-8 -*-
# Date:2025-01-24 10 27
# -*- coding: utf-8 -*-
import httpx
from argon_log import logger
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


class RequestHandler:
    def __init__(
        self, headers: Dict[str, str], cookies: Optional[Dict[str, str]] = None
    ):
        """
        初始化 RequestHandler。

        :param headers: 请求头
        :param cookies: 请求 cookies（可选）
        """
        self.headers = headers
        self.cookies = cookies or {}

    # 重试配置
    async def fetch_data_get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
    ) -> Optional[httpx.Response]:
        """
        发送 HTTP GET 请求并返回响应内容。

        :param url: 请求的 URL
        :param params: 请求参数（可选）
        :param headers: 临时请求头（可选）
        :param cookies: 临时请求 cookies（可选）
        :return: 响应内容（字符串）
        """
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                response = await client.get(
                    url,
                    headers=headers or self.headers,
                    cookies=cookies or self.cookies,
                    params=params,
                )
                response.raise_for_status()
                return response
        except httpx.HTTPStatusError as e:
            logger.error(f"GET 请求失败，状态码: {e.response.status_code}, URL: {url}")
        except Exception as e:
            logger.error(f"GET 请求时发生错误: {e}, URL: {url}")
        return None

    # 重试配置
    @retry(
        stop=stop_after_attempt(3),  # 最多重试 3 次
        wait=wait_fixed(1),  # 每次重试间隔 1 秒
        retry=retry_if_exception_type(
            (httpx.HTTPStatusError, Exception)
        ),  # 仅在 HTTP 错误或请求错误时重试
    )
    async def fetch_data_post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
    ) -> Optional[httpx.Response]:
        """
        发送 HTTP POST 请求并返回响应内容。

        :param url: 请求的 URL
        :param data: 表单数据（可选）
        :param json: JSON 数据（可选）
        :param headers: 临时请求头（可选）
        :param cookies: 临时请求 cookies（可选）
        :return: 响应内容（字符串）
        """
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                response = await client.post(
                    url,
                    headers=headers or self.headers,
                    cookies=cookies or self.cookies,
                    data=data,
                    json=json,
                )
                response.raise_for_status()
                return response
        except httpx.HTTPStatusError as e:
            logger.error(f"POST 请求失败，状态码: {e.response.status_code}, URL: {url}")
        except Exception as e:
            logger.error(f"POST 请求时发生错误: {e}, URL: {url}")
        return None

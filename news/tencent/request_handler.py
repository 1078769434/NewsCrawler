# -*- coding: utf-8 -*-
import httpx
from argon_log import logger
from typing import Optional


class RequestHandler:
    def __init__(self):
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://news.qq.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://news.qq.com/",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        }
        self.cookies = {
            "pgv_pvid": "5700020769",
            "ptcz": "6f3878d04c058028ae213e97130ba140028cc0d85a3ae89a7bb02671ca0e8c4a",
            "_qimei_q36": "",
            "_qimei_h38": "2db8ae78169faf2822dc82c30200000ad17b01",
            "_clck": "3922571152|1|fo9|0",
            "LW_uid": "w1T7K2Y5H3o7a0f844f8e249L9",
            "eas_sid": "M1d732W5X3G7S0R8j4K899b427",
            "RK": "ds0oBt+SHN",
            "LW_sid": "z1G7S3x5d9N7d399Q336i2X2N1",
            "pac_uid": "0_FpZFnxfEm2k23",
            "current-city-name": "bj",
            "_qimei_fingerprint": "76246fe3d383bbb144b907797058915d",
            "_qimei_uuid42": "191140d03381002c05f860db197bad5045ea284aab",
            "pgv_info": "ssid=s5804477246",
            "ts_last": "news.qq.com/index_nav2_mod.htm",
            "ts_refer": "www.bing.com/",
            "ts_uid": "8351931226",
            "suid": "user_0_FpZFnxfEm2k23",
            "lcad_o_minduid": "TOQtdWY__htIyOwAUyUZXjEGO1VlQTmI",
            "lcad_appuser": "5D144067DA8F27BE",
            "lcad_LPPBturn": "557",
            "lcad_LPSJturn": "187",
            "lcad_LBSturn": "342",
            "lcad_LVINturn": "68",
            "lcad_LDERturn": "260",
        }

    async def fetch_post_data(
        self, url: str, data: dict | str = None
    ) -> Optional[dict]:
        """
        发送 HTTP 请求并返回响应内容。

        :param data: 请求体
        :param url: 请求的 URL
        :param params: 请求参数
        :return: 响应内容（字符串）
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    url, headers=self.headers, cookies=self.cookies, data=data
                )
                response.raise_for_status()  # 检查请求是否成功
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"请求失败，状态码: {e.response.status_code}, URL: {url}")
        except Exception as e:
            logger.error(f"请求时发生错误: {e}, URL: {url}")
        return None

    async def fetch_data(self, url: str, params: dict = None) -> Optional[str]:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
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

# -*- coding: utf-8 -*-
# Date:2025-01-24 15 17
# dingtalk_notifier.py
import httpx
import json
import time
import hmac
import hashlib
import base64
from urllib.parse import quote_plus
from argon_log import logger


class DingTalkNotifier:
    def __init__(self, webhook_url: str, secret: str = None, enabled: bool = False):
        """
        初始化钉钉通知器。

        :param webhook_url: 钉钉机器人的 Webhook URL
        :param secret: 钉钉机器人的加签密钥（可选）
        """
        self.webhook_url = webhook_url
        self.secret = secret
        self.enabled = enabled

    async def send_markdown_message(self, title: str, text: str):
        """
        发送 Markdown 格式的消息到钉钉群。

        :param title: 消息标题
        :param text: 消息内容（Markdown 格式）
        """
        if not self.enabled:
            logger.info("钉钉通知未开启，跳过发送消息。")
            return
        try:
            # 构造消息体
            message = {
                "msgtype": "markdown",
                "markdown": {"title": title, "text": text},
            }

            # 生成签名并构造最终的 Webhook URL
            url = self._generate_signed_url()

            # 发送请求
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    content=json.dumps(message),
                )

            # 检查响应
            if response.status_code == 200:
                logger.info(f"钉钉通知发送成功: {title}")
            else:
                logger.error(f"钉钉通知发送失败: {response.text}")
        except Exception as e:
            logger.error(f"发送钉钉通知时发生错误: {e}")

    async def send_combined_news_notification(
        self, news_list: list, title: str = "新闻汇总"
    ):
        """
        将多条新闻整合成一个消息并发送到钉钉群。

        :param news_list: 新闻列表，每条新闻应包含 title 和 url 字段
        :param title: 消息标题，默认为 "新闻汇总"
        """
        if not news_list:
            logger.warning("没有可发送的新闻内容。")
            return

        # 构造消息内容
        text = f"# 🚀 {title}\n\n"
        for index, news in enumerate(news_list, start=1):
            # 将链接映射到标题上
            news_title = news.get("title", "无标题")
            news_url = news.get("url", "")
            text += f"{index}. [{news_title}]({news_url})\n\n"

        # 发送整合后的消息
        await self.send_markdown_message(title, text)

    def _generate_signed_url(self) -> str:
        """
        生成带签名的 Webhook URL。

        :return: 带签名的 Webhook URL
        """
        if not self.secret:
            return self.webhook_url

        # 获取当前时间戳（单位：毫秒）
        timestamp = str(round(time.time() * 1000))

        # 构造签名字符串
        secret_enc = self.secret.encode("utf-8")
        string_to_sign = f"{timestamp}\n{self.secret}"
        string_to_sign_enc = string_to_sign.encode("utf-8")

        # 使用 HMAC-SHA256 算法生成签名
        hmac_code = hmac.new(
            secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
        ).digest()

        # 对签名进行 Base64 编码和 URL 编码
        sign = quote_plus(base64.b64encode(hmac_code))

        # 构造带签名的 URL
        signed_url = f"{self.webhook_url}&timestamp={timestamp}&sign={sign}"
        return signed_url

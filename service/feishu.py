# -*- coding: utf-8 -*-
# Date:2025-04-03 16 40
# -*- coding: utf-8 -*-
# Date: 2025-01-24
# feishu_notifier.py
import httpx
import json
import time
import hmac
import hashlib
import base64
from urllib.parse import quote_plus
from argon_log import logger


class FeishuNotifier:
    def __init__(self, webhook_url: str, secret: str = None, enabled: bool = False):
        """
        初始化飞书通知器。

        :param webhook_url: 飞书机器人的 Webhook URL
        :param secret: 机器人安全设置中的加签密钥（可选）
        :param enabled: 是否启用通知
        """
        self.webhook_url = webhook_url
        self.secret = secret
        self.enabled = enabled

    async def send_text_message(self, content: str):
        """
        发送文本消息到飞书群。

        :param content: 消息内容
        """
        if not self.enabled:
            logger.info("飞书通知未开启，跳过发送消息。")
            return

        try:
            message = {"msg_type": "text", "content": {"text": content}}
            url = self._generate_signed_url()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    content=json.dumps(message),
                )

            if response.status_code == 200:
                logger.info(f"飞书通知发送成功: {content}")
            else:
                logger.error(f"飞书通知发送失败: {response.text}")
        except Exception as e:
            logger.error(f"发送飞书通知时发生错误: {e}")

    async def send_markdown_message(self, title: str, text: str):
        """
        发送富文本（post）消息，支持超链接显示。

        :param title: 消息标题
        :param text: 内容，可包含 Markdown 风格 [title](url)
        """
        if not self.enabled:
            logger.info("飞书通知未开启，跳过发送消息。")
            return

        try:
            lines = text.strip().splitlines()
            content_blocks = []

            for line in lines:
                if not line.strip():
                    continue

                # 检查是否是 Markdown 链接格式 [文本](链接)
                if line.strip().startswith("[") and "](" in line:
                    import re

                    match = re.match(r"\[(.*?)\]\((.*?)\)", line.strip())
                    if match:
                        link_text = match.group(1)
                        link_url = match.group(2)
                        content_blocks.append(
                            {"tag": "a", "text": link_text, "href": link_url}
                        )
                        continue

                # 否则按普通文本处理
                content_blocks.append({"tag": "text", "text": line + "\n"})

            message = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": title,
                            "content": [content_blocks],
                        }
                    }
                },
            }

            url = self._generate_signed_url()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    content=json.dumps(message),
                )

            if response.status_code == 200:
                logger.info(f"飞书 Markdown 通知发送成功: {title}")
            else:
                logger.error(f"飞书 Markdown 通知发送失败: {response.text}")
        except Exception as e:
            logger.error(f"发送飞书 Markdown 通知时发生错误: {e}")

    async def send_combined_news_notification(
        self, news_list: list, title: str = "📰 新闻汇总", at_all: bool = True
    ):
        """
        发送多条新闻整合成一个飞书 post 富文本消息，每条新闻带链接，自动换行。
        :param news_list: 新闻列表，每条应包含 title 和 url 字段
        :param title: 通知标题
        :param at_all: @所有人
        """
        if not self.enabled:
            logger.info("飞书通知未开启，跳过发送消息。")
            return

        if not news_list:
            logger.warning("没有可发送的新闻内容。")
            return

        try:
            content_blocks = []

            # 首段：标题 + @所有人
            first_block = [{"tag": "text", "text": f"🚀 {title}"}]
            if at_all:
                first_block.append({"tag": "text", "text": " "})
                first_block.append({"tag": "at", "user_id": "all"})
            content_blocks.append(first_block)

            # 添加每条新闻（每条作为一段）
            for idx, news in enumerate(news_list, start=1):
                news_title = news.get("title", "无标题")
                news_url = news.get("url", "#")
                block = [{"tag": "a", "text": f"{idx}. {news_title}", "href": news_url}]
                content_blocks.append(block)  # 每条新闻作为一个段落

            message = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": title,
                            "content": content_blocks,
                        }
                    }
                },
            }

            url = self._generate_signed_url()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    content=json.dumps(message),
                )

            if response.status_code == 200:
                logger.info(f"飞书 Markdown 通知发送成功: {title}")
            else:
                logger.error(f"飞书 Markdown 通知发送失败: {response.text}")
        except Exception as e:
            logger.error(f"发送飞书 Markdown 通知时发生错误: {e}")

    def _generate_signed_url(self) -> str:
        """
        生成带签名的 Webhook URL（适用于启用了“加签”安全设置的飞书机器人）。

        :return: 带签名的 Webhook URL
        """
        if not self.secret:
            return self.webhook_url

        timestamp = str(int(time.time()))
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            self.secret.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        sign = base64.b64encode(hmac_code).decode("utf-8")

        signed_url = f"{self.webhook_url}&timestamp={timestamp}&sign={quote_plus(sign)}"
        return signed_url

    async def send_multi_news_card(
        self,
        news_list: list,
        card_title: str = "📰 每日新闻速递",
        card_color: str = "wathet",
        at_all: bool = True,
        group_size: int = 5,
        show_more_button: bool = True,
        more_button_url: str = "https://news.baidu.com",
    ):
        """
        发送多条新闻的交互式卡片消息

        :param news_list: 新闻列表，每个元素应包含title和url字段，可包含desc字段
        :param card_title: 卡片标题
        :param card_color: 卡片颜色模板(blue/wathet/turquoise/green/yellow/orange/red/purple)
        :param at_all: 是否@所有人
        :param group_size: 每组显示的新闻数量(飞书建议不超过10条)
        :param show_more_button: 是否显示"查看更多"按钮
        :param more_button_url: "查看更多"按钮的链接
        """
        if not self.enabled:
            logger.info("飞书通知未开启，跳过发送卡片消息。")
            return

        if not news_list:
            logger.warning("没有可发送的新闻内容。")
            return

        try:
            elements = []

            # 添加@所有人
            if at_all:
                elements.append(
                    {"tag": "markdown", "content": '<at user_id="all">所有人</at>'}
                )
            # 添加分隔线
            elements.append({"tag": "hr"})

            # 分组添加新闻条目
            for i in range(0, len(news_list), group_size):
                group = news_list[i : i + group_size]

                for idx, news in enumerate(group, start=i + 1):
                    title = news.get("title", "无标题")
                    url = news.get("url", "#")
                    desc = news.get("desc")

                    # 新闻条目
                    news_element = {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"{idx}. [{title}]({url})"
                            + (f"\n   *{desc}*" if desc else ""),
                        },
                    }
                    elements.append(news_element)

                # 如果不是最后一组，添加分隔线
                if i + group_size < len(news_list):
                    elements.append({"tag": "hr"})

            # 添加底部按钮
            if show_more_button:
                elements.append({"tag": "hr"})
                elements.append(
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "查看更多新闻",
                                },
                                "type": "primary",
                                "url": more_button_url,
                            }
                        ],
                    }
                )

            # 构建完整卡片
            message = {
                "msg_type": "interactive",
                "card": {
                    "config": {"wide_screen_mode": True, "enable_forward": True},
                    "header": {
                        "title": {"tag": "plain_text", "content": card_title},
                        "template": card_color,
                    },
                    "elements": elements,
                },
            }

            url = self._generate_signed_url()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    content=json.dumps(message),
                )

            if response.status_code == 200:
                logger.info(
                    f"多条新闻卡片发送成功:{response.json()}，共{len(news_list)}条新闻"
                )
            else:
                logger.error(f"多条新闻卡片发送失败: {response.text}")
        except Exception as e:
            logger.error(f"发送多条新闻卡片出错: {e}")

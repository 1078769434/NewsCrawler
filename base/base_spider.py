# -*- coding: utf-8 -*-
# Date:2025-01-24 10 15
import abc

from config import settings
from save.database_handler import DatabaseHandler
from save.storage import NewsStorage
from service.dingding import DingTalkNotifier
from service.feishu import FeishuNotifier


class BaseSpider(abc.ABC):
    def __init__(self):
        self.dingtalk_notifier = DingTalkNotifier(
            webhook_url=settings.dingtalk.webhook_url,  # 替换为你的钉钉 Webhook URL
            secret=settings.dingtalk.secret,  # 替换为你的钉钉密钥
            enabled=settings.dingtalk.enabled,  # 是否开启钉钉通知
        )

        # 初始化 Feishu 通知器
        self.feishu_talk_notifier = FeishuNotifier(
            webhook_url=settings.feishutalk.webhook_url,
            secret=settings.feishutalk.secret,
            enabled=settings.feishutalk.enabled,
        )

        # 初始化保存器
        self.storage_enabled = settings.storage.enabled
        self.to_database = settings.storage.to_database
        self.storage_handler = NewsStorage(output_format=settings.storage.output_format)

        # 初始化数据库处理器
        self.database_handler = DatabaseHandler()

    # 获取热门新闻
    @abc.abstractmethod
    async def fetch_hot_news(self):
        pass

    # 获取最新国内新闻
    @abc.abstractmethod
    async def fetch_latest_china_news(self):
        pass

    # 获取新闻并处理
    @abc.abstractmethod
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
        :param category: 新闻分类
        :param source: 新闻来源
        :param log_prefix: 日志前缀
        :param parse_method: 解析数据的方法
        """
        pass

    # 处理单条新闻
    @abc.abstractmethod
    async def process_news(self, news):
        pass

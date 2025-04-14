# -*- coding: utf-8 -*-
# Date:2025-01-24 10 15
import abc


class BaseSpider(abc.ABC):
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

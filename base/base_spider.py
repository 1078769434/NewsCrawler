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
    async def fetch_and_process_news(self):
        pass

    # 处理单条新闻
    @abc.abstractmethod
    async def process_news(self, news):
        pass

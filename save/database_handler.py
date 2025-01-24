from typing import List, Dict
from model import News
from db.session import get_db
from argon_log import logger
from utils.spider_tools import convert_to_datetime
from sqlalchemy import select


class DatabaseHandler:
    async def insert_or_update_news(
        self, news_data: Dict | List[Dict], category: str, source: str
    ) -> None:
        """
        插入或更新新闻数据到数据库（支持单条或批量操作）。

        :param news_data: 单条新闻数据（字典）或新闻数据列表（列表）
        :param category: 新闻分类（"hot" 或 "latest_china"）
        :param source: 新闻来源网站（"sina"、"tencent" 或 "other"）
        """
        async for db in get_db():  # 获取异步数据库会话
            try:
                # 判断是单条数据还是批量数据
                if isinstance(news_data, list):
                    await self._batch_insert_or_update_news(
                        db, news_data, category, source
                    )
                else:
                    await self._single_insert_or_update_news(
                        db, news_data, category, source
                    )
            except Exception as e:
                await db.rollback()  # 回滚事务
                logger.error(f"新闻数据操作失败：{e}")
            finally:
                await db.close()

    async def _single_insert_or_update_news(
        self, db, news_data: Dict, category: str, source: str
    ) -> None:
        """
        插入或更新单条新闻数据到数据库。

        :param db: 数据库会话
        :param news_data: 单条新闻数据（字典）
        :param category: 新闻分类
        :param source: 新闻来源
        """
        # 查询数据库，检查是否已存在相同的记录
        existing_record = await db.execute(
            select(News).where(News.url == news_data.get("url"))
        )
        existing_record = existing_record.scalar_one_or_none()
        if existing_record:
            # 如果记录已存在，更新字段
            existing_record.title = news_data.get("title")
            existing_record.content = news_data.get("content")
            existing_record.author = news_data.get("author")
            existing_record.media_name = news_data.get("meta").get("mediaid")
            existing_record.intro = news_data.get("meta").get("description")
            existing_record.publish_time = convert_to_datetime(
                news_data.get("publish_time")
            )
            existing_record.images = str(news_data.get("images"))
            existing_record.category = category
            existing_record.source = source
            logger.info(f"新闻数据更新成功：{existing_record.title}")
        else:
            # 如果记录不存在，创建新的 ORM 对象
            news = News(
                title=news_data.get("title"),
                url=news_data.get("url"),  # URL 是唯一标识
                content=news_data.get("content"),
                author=news_data.get("author"),
                media_name=news_data.get("meta").get("mediaid"),
                intro=news_data.get("meta").get("description"),
                publish_time=convert_to_datetime(news_data.get("publish_time")),
                images=str(news_data.get("images")),
                category=category,
                source=source,
            )
            # 添加新记录
            db.add(news)
            logger.info(f"新闻数据插入成功：{news.title}")
        # 提交事务
        await db.commit()

    async def _batch_insert_or_update_news(
        self, db, news_data_list: List[Dict], category: str, source: str
    ) -> None:
        """
        批量插入或更新新闻数据到数据库。

        :param db: 数据库会话
        :param news_data_list: 新闻数据列表
        :param category: 新闻分类
        :param source: 新闻来源
        """
        for news_data in news_data_list:
            # 查询数据库，检查是否已存在相同的记录
            existing_record = await db.execute(
                select(News).where(News.url == news_data.get("url"))
            )
            existing_record = existing_record.scalar_one_or_none()
            if existing_record:
                # 如果记录已存在，更新字段
                existing_record.title = news_data.get("title")
                existing_record.content = news_data.get("content")
                existing_record.author = news_data.get("author")
                existing_record.media_name = news_data.get("meta").get("mediaid")
                existing_record.intro = news_data.get("meta").get("description")
                existing_record.publish_time = convert_to_datetime(
                    news_data.get("publish_time")
                )
                existing_record.images = str(news_data.get("images"))
                existing_record.category = category
                existing_record.source = source
                logger.info(
                    f"新闻数据更新成功-新闻发布时间{existing_record.publish_time}：{existing_record.title}"
                )
            else:
                # 如果记录不存在，创建新的 ORM 对象
                news = News(
                    title=news_data.get("title"),
                    url=news_data.get("url"),  # URL 是唯一标识
                    content=news_data.get("content"),
                    author=news_data.get("author"),
                    media_name=news_data.get("meta").get("mediaid"),
                    intro=news_data.get("meta").get("description"),
                    publish_time=convert_to_datetime(news_data.get("publish_time")),
                    images=str(news_data.get("images")),
                    category=category,
                    source=source,
                )
                # 添加新记录
                db.add(news)
                logger.info(
                    f"新闻数据插入成功-新闻发布时间{news.publish_time}：{news.title}"
                )
        # 提交事务
        await db.commit()

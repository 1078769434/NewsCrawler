from sqlalchemy import Column, Integer, String, Text, DateTime, func, UniqueConstraint

from db.session import Base

from enum import Enum

import sqlalchemy as sa


class NewsCategory(Enum):
    """
    新闻分类枚举类。
    """

    # 热点新闻
    HOT = "hot"
    # 国内最新新闻
    LATEST_CHINA = "latest_china"
    # 国际最新新闻
    LATEST_INTERNATIONAL = "latest_international"


class Source(Enum):
    """
    新闻来源枚举类。
    """

    # 新浪新闻
    SINA = "sina"
    # 腾讯新闻
    TENCENT = "tencent"
    # 网易新闻
    NETEASE = "netease"
    # 央视新闻
    CCTV = "cctv"
    # 今日头条
    TOUTIAO = "toutiao"
    # 百度新闻
    BAIDU = "baidu"
    # 澎湃新闻
    THE_PAPER = "the_paper"
    # 知乎
    ZHIHU = "zhihu"
    # 微博
    WEIBO = "weibo"
    # 凤凰新闻
    FENG_HUANG = "feng_huang"


class News(Base):
    """
    新闻 ORM 模型。
    """

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="新闻标题")
    url = Column(String(255), nullable=False, unique=True, comment="新闻链接")
    content = Column(Text, nullable=True, comment="新闻内容")
    author = Column(String(100), nullable=True, comment="新闻作者")
    intro = Column(Text, nullable=True, comment="新闻简介")
    publish_time = Column(DateTime, nullable=True, comment="发布时间")
    media_name = Column(String(100), nullable=True, comment="媒体名称")
    images = Column(Text, nullable=True, comment="图片列表")
    category = Column(
        sa.Enum(
            NewsCategory, values_callable=lambda x: [e.value for e in NewsCategory]
        ),
        nullable=False,
        comment="新闻分类",
    )
    source = Column(
        sa.Enum(Source, values_callable=lambda x: [e.value for e in Source]),
        nullable=False,
        comment="新闻来源网站",
    )
    create_time = Column(
        DateTime, nullable=True, default=func.now(), comment="采集创建时间"
    )
    update_time = Column(
        DateTime, nullable=True, default=func.now(), comment="采集更新时间"
    )

    # 添加唯一约束
    __table_args__ = (UniqueConstraint("url", name="uq_news_url"),)

from sqlalchemy import Column, Integer, String, Text, Enum, DATE, func

from db.session import Base


class News(Base):
    """
    新闻 ORM 模型。
    """

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="新闻标题")
    url = Column(String(255), nullable=False, comment="新闻链接")
    content = Column(Text, nullable=True, comment="新闻内容")
    author = Column(String(100), nullable=True, comment="新闻作者")
    media = Column(String(100), nullable=True, comment="媒体名称")
    intro = Column(Text, nullable=True, comment="新闻简介")
    publish_time = Column(DATE, nullable=True, comment="发布时间")
    media_name = Column(String(100), nullable=True, comment="媒体名称")
    images = Column(Text, nullable=True, comment="图片列表")
    category = Column(Enum("hot", "latest_china"), nullable=False, comment="新闻分类")
    source = Column(
        Enum("sina", "tencent", "other"), nullable=False, comment="新闻来源网站"
    )
    create_time = Column(
        DATE, nullable=True, default=func.now(), comment="采集创建时间"
    )
    update_time = Column(
        DATE, nullable=True, default=func.now(), comment="采集更新时间"
    )

    def __repr__(self):
        """
        返回对象的字符串表示形式，用于调试和日志记录。
        """
        return (
            f"<News(id={self.id}, title={self.title}, url={self.url}, "
            f"category={self.category}, source={self.source}, "
            f"create_time={self.create_time}, update_time={self.update_time})>"
        )

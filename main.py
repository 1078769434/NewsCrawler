import argparse
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from news.baidu.baidu_crawl import BaiduNewsSpider
from news.cctv.cctv_crawl import CCTVNewsSpider
from news.netease.netease_crawl import NeteaseNewsSpider
from news.sina.sina_crawl import SinaNewsSpider
from news.tencent.tencent_crawl import TencentNewsSpider
from news.toutiao.toutiao_crawl import ToutiaoNewsSpider
from argon_log import logger, init_logging

init_logging()


async def run_spider(spider_name: str, news_type: str):
    """
    根据爬虫名称和新闻类型运行对应的爬虫。

    :param spider_name: 爬虫名称（如 "cctv" 或 "netease"）
    :param news_type: 新闻类型（如 "hot_news" 或 "latest_china_news"）
    """
    if spider_name == "cctv":
        spider = CCTVNewsSpider()
    elif spider_name == "netease":
        spider = NeteaseNewsSpider()
    elif spider_name == "sina":
        spider = SinaNewsSpider()
    elif spider_name == "tencent":
        spider = TencentNewsSpider()
    elif spider_name == "toutiao":
        spider = ToutiaoNewsSpider()
    elif spider_name == "baidu":
        spider = BaiduNewsSpider()
    else:
        raise ValueError(f"未知的爬虫名称: {spider_name}")

    # 根据新闻类型调用对应的方法
    if news_type == "hot_news":
        await spider.fetch_hot_news()
    elif news_type == "latest_china_news":
        await spider.fetch_latest_china_news()
    else:
        raise ValueError(f"未知的新闻类型: {news_type}")


async def scheduled_task(spider_name: str, news_type: str, interval: int):
    """
    定时任务：每隔指定时间运行一次爬虫。

    :param spider_name: 爬虫名称
    :param news_type: 新闻类型
    :param interval: 定时任务的间隔时间（单位：分钟）
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_spider,
        trigger=IntervalTrigger(minutes=interval),
        args=[spider_name, news_type],
        next_run_time=datetime.now(),  # 立即运行一次
    )
    scheduler.start()
    logger.info(f"定时任务已启动，每隔 {interval} 分钟运行一次爬虫 {spider_name}。")

    try:
        # 保持事件循环运行
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("定时任务已停止。")
        scheduler.shutdown()


def main():
    """
    主程序入口：解析命令行参数并启动对应的爬虫或定时任务。
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="新闻爬虫主程序")
    parser.add_argument(
        "--spider",
        type=str,
        required=True,
        choices=["cctv", "netease", "sina", "tencent", "toutiao"],
        help="指定要运行的爬虫（如 'cctv' 或 'netease'）",
    )
    parser.add_argument(
        "--news-type",
        type=str,
        required=True,
        choices=["hot_news", "latest_china_news"],
        help="指定要抓取的新闻类型（如 'hot_news' 或 'latest_china_news'）",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=None,
        help="定时任务的间隔时间（单位：分钟）。如果不指定，则只运行一次。",
    )
    args = parser.parse_args()

    # 运行爬虫
    try:
        if args.interval:
            # 启动定时任务
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                scheduled_task(args.spider, args.news_type, args.interval)
            )
        else:
            # 只运行一次
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run_spider(args.spider, args.news_type))
    except Exception as e:
        logger.error(f"爬虫运行失败: {e}")


if __name__ == "__main__":
    main()

import asyncio

from news.sina.sina_crawl import SinaNewsSpider


async def run_spider():
    """
    主爬虫函数：初始化爬虫并运行。
    """
    spider = SinaNewsSpider()
    await spider.fetch_latest_china_news()
    await spider.fetch_hot_news()


def main():
    """
    程序入口：运行主爬虫函数。
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_spider())


if __name__ == "__main__":
    main()

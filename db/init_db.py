import asyncio

from loguru import logger
from sqlalchemy import inspect

# ⚠️ warning  import register model here, your class must  import in models.__init__.py file
import model  # noqa: F401

from db.session import async_engine, Base


async def async_main():
    async with async_engine.begin() as conn:
        logger.info("Drop tables")
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Create tables success")
        await conn.run_sync(Base.metadata.create_all)


async def async_init_db():
    async with async_engine.begin() as conn:
        # 使用 run_sync 执行同步操作
        inspector = await conn.run_sync(inspect)
        existing_tables = inspector.get_table_names()

        # 如果没有找到任何表，表示数据库为空，才进行表创建
        if not existing_tables:
            logger.info("未找到表，正在创建表...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("表创建成功。")
        else:
            logger.info("表已存在，跳过创建。")


if __name__ == "__main__":
    asyncio.run(async_init_db())

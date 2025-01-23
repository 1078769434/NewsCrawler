import asyncio

from loguru import logger

# ⚠️ warning  import register model here, your class must  import in models.__init__.py file
import model  # noqa: F401

from db.session import async_engine, Base


async def async_main():
    async with async_engine.begin() as conn:
        logger.info("Drop tables")
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Create tables success")
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(async_main())

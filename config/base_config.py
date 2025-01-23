from pathlib import Path
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from argon_log import logger

# 项目根目录
PROJECT_DIR: Path = Path(__file__).resolve().parent.parent

# 配置文件路径
CONFIG_FILE_PATH: Path = PROJECT_DIR / "config.yaml"
CONFIG_DEV_FILE_PATH: Path = PROJECT_DIR / "config_dev.yaml"


class Settings(BaseSettings):
    PROJECT_DIR: Path = PROJECT_DIR
    # sqlalchemy echo
    SQLALCHEMY_ECHO: bool = False

    MYSQL_DATABASE_URL: str = "mysql+aiomysql://root:password@localhost:3306/news_db"

    # 从 YAML 文件加载配置
    @classmethod
    def from_yaml(cls, config_file: Path) -> "Settings":
        """
        从 YAML 文件加载配置。

        :param config_file: YAML 配置文件路径
        :return: Settings 实例
        """
        with open(config_file, "r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)
        return cls(**config_data)

    # Pydantic 配置
    model_config = SettingsConfigDict(extra="ignore")


def load_settings() -> Settings:
    """
    加载配置文件，优先读取 config_dev.yaml，如果不存在则读取 config.yaml。

    :return: Settings 实例
    """
    if CONFIG_DEV_FILE_PATH.exists():
        logger.info("加载开发环境配置文件：config_dev.yaml")
        return Settings.from_yaml(CONFIG_DEV_FILE_PATH)
    elif CONFIG_FILE_PATH.exists():
        logger.info("加载默认配置文件：config.yaml")
        return Settings.from_yaml(CONFIG_FILE_PATH)
    else:
        raise FileNotFoundError("未找到配置文件：config_dev.yaml 或 config.yaml")


# 加载配置并缓存到模块级变量
settings: Settings = load_settings()

if __name__ == "__main__":
    print(settings.model_dump())

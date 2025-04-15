from pathlib import Path
import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录
PROJECT_DIR: Path = Path(__file__).resolve().parent.parent

# 配置文件路径
CONFIG_FILE_PATH: Path = PROJECT_DIR / "config.yaml"
CONFIG_DEV_FILE_PATH: Path = PROJECT_DIR / "config_dev.yaml"


# 嵌套配置模型
class MySQLConfig(BaseModel):
    database_url: str = "mysql+aiomysql://root:password@localhost:3306/news_db"


class LoggingConfig(BaseModel):
    level: str = "INFO"


class DingTalkConfig(BaseModel):
    enabled: bool = True
    webhook_url: str = "https://oapi.dingtalk.com/robot/send?access_token="
    secret: str = None  # 可选字段


class FeiShuConfig(BaseModel):
    enabled: bool = True
    webhook_url: str = ""
    secret: str = None  # 可选字段


class NewsStorageConfig(BaseModel):
    enabled: bool = False  # 默认为不开启
    output_format: str = "json"  # 默认使用 JSON，可以配置为 "csv"
    to_database: bool = False  # ✅ 是否保存到数据库，默认不开启


class Settings(BaseSettings):
    PROJECT_DIR: Path = PROJECT_DIR
    SQLALCHEMY_ECHO: bool = False

    # 嵌套配置
    mysql: MySQLConfig = MySQLConfig()
    logging: LoggingConfig = LoggingConfig()
    dingtalk: DingTalkConfig = DingTalkConfig()
    feishutalk: FeiShuConfig = FeiShuConfig()
    storage: NewsStorageConfig = NewsStorageConfig()

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
        return Settings.from_yaml(CONFIG_DEV_FILE_PATH)
    elif CONFIG_FILE_PATH.exists():
        return Settings.from_yaml(CONFIG_FILE_PATH)
    else:
        raise FileNotFoundError("未找到配置文件：config_dev.yaml 或 config.yaml")


# 加载配置并缓存到模块级变量
settings: Settings = load_settings()

if __name__ == "__main__":
    print(settings.model_dump())

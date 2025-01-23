import random

import uuid
import time
from datetime import datetime, timedelta


def get_random_headers():
    """
    生成随机的请求头

    Returns:
        dict: 包含随机 User-Agent 的请求头
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
    }
    return headers


def generate_hex_uuid_v1():
    """
    生成一个十六进制的 UUID v1。

    返回值:
        str: 十六进制的 UUID v1 字符串，不包含连字符。
    """
    # 生成 UUID v1
    uuid_v1 = uuid.uuid1()

    # 转换为十六进制字符串，并去掉连字符
    hex_uuid = uuid_v1.hex

    return hex_uuid


def generate_timestamp():
    """
    生成当前时间的时间戳（毫秒级）。

    :return: 时间戳字符串
    """
    # 获取当前时间的秒级时间戳
    timestamp = int(time.time() * 1000)  # 乘以 1000 转换为毫秒
    return str(timestamp)


def generate_top_time(days_offset: int = 0) -> str:
    """
    生成指定日期的 `top_time` 参数（格式为 `YYYYMMDD`）。

    :param days_offset: 日期偏移量（默认为 0，表示今天）
    :return: 格式化后的日期字符串（例如 "20250122"）
    """
    # 获取当前日期
    today = datetime.now()
    # 根据偏移量计算目标日期
    target_date = today + timedelta(days=days_offset)
    # 格式化日期为 `YYYYMMDD`
    return target_date.strftime("%Y%m%d")

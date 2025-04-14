# -*- coding: utf-8 -*-
# Date:2025-04-14 15 54
from base.base_request import RequestHandler

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "mweibo-pwa": "1",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://m.weibo.cn/p/index?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&luicode=20000061&lfid=5070140584495876",
    "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "fecb39",
}
cookies = {
    "_T_WM": "28666720942",
    "XSRF-TOKEN": "fecb39",
    "WEIBOCN_FROM": "1110006030",
    "MLOGIN": "0",
    "M_WEIBOCN_PARAMS": "luicode%3D20000061%26lfid%3D5070140584495876%26fid%3D106003type%253D25%2526t%253D3%2526disable_hot%253D1%2526filter_type%253Drealtimehot%26uicode%3D10000011",
    "mweibo_short_token": "f5feecf312",
}
weibo_request_handler = RequestHandler(headers, cookies)

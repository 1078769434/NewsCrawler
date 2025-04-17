# -*- coding: utf-8 -*-
from base.base_request import RequestHandler

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://news.sina.com.cn/china/",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
}
cookies = {
    "rotatecount": "1",
    "UOR": "www.bing.com,news.sina.com.cn,",
    "SINAGLOBAL": "120.224.113.145_1737594794.479271",
    "Apache": "120.224.113.145_1737594794.479272",
    "SUB": "_2AkMQzRjcf8NxqwFRmfoWzG7ia4RxzwrEieKmkekHJRMyHRl-yD9kqmgotRB6O002MxSnB-7ZXhqOwccJh8YXwvcNFOqE",
    "SUBP": "0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFMSKeYDNiQlbyDJ1HuHHnd",
    "directAd_samsung": "true",
    "ULV": "1737594902732:2:2:2:120.224.113.145_1737594794.479272:1737594791231",
}
sina_request_handler = RequestHandler(headers=headers)

# -*- coding: utf-8 -*-
# Date:2025-04-11 17 12
from base.base_request import RequestHandler

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "client-type": "1",
    "origin": "https://www.thepaper.cn",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.thepaper.cn/",
    "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
}
cookies = {
    "Hm_lvt_94a1e06bbce219d29285cee2e37d1d26": "1744610629",
    "HMACCOUNT": "A526A7800166442B",
    "ariaDefaultTheme": "undefined",
    "Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26": "1744610673",
    "tfstk": "gICst2qImcm1SbnhSlUePKn6t-AfliNrGqTArZhZkCdtDmQJYjS4SIRfkg72H1726VXh4ahN_RAqGCADMurza7zGSIAxSzm8Uhbd-EUeWyqVcqODMureeorWoIjua9pNBwUBuE8t6ipT9wKHzAdvXKnKpUKpDIIvDpdpyUkt6KKtpyTDvndvMidKTbqB-RtO5P02eBEsj379AjhA9Sv6VNHqMjCB5d1AWH_N76T6C3pe-rR56M7A_1v3EYRc8TsfHMFI1i_OeiKN9uhX0TYfkUO8Z4td1Z1BI9otBUO6fLC9p4lFJKBCOC5TmYbFRhpWT9y3bKR1fTxkBJqhcwtND19Kfk-VUw59dgEEOivfBGTpwgRia3gK-xgBEjTB4yaInx2P4vbK93FimdLH8_zQRcMDBeYB4yaInxv9-eJzRyisn",
}
the_paper_request_handler = RequestHandler(headers=headers, cookies=cookies)

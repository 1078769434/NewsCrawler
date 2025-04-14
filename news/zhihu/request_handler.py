# -*- coding: utf-8 -*-
# Date:2025-04-14 14 44
from base.base_request import RequestHandler

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
}
cookies = {
    "q_c1": "68e3a76b187540c0879dbafd315ebad8|1718820150000|1693300214000",
    "dream_token": "ZmRkZjFhMDY1Zjg0ZmRkM2YzODlkN2U0ZjcxNThjZjcxOTg3MWZmMTE0ZjUzNDZkMDM5MTlhYTA5OGNlY2IwNw==",
    "_zap": "df87f5b7-785e-4222-b9c0-0ccff97423c4",
    "d_c0": "ADDS2be5ohmPTivBF6K_oX-8FajxozYS_MM=|1733197050",
    "edu_user_uuid": "edu-v1|a5ca96aa-a5fc-489e-bacf-dfffa79e5856",
    "_xsrf": "xGAE4IvHlxmuOR2YmQcp4THTGvteYPMh",
    "Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49": "1744162381,1744353333,1744446879,1744595192",
    "HMACCOUNT": "A526A7800166442B",
    "SESSIONID": "ixOVufClhDVRQX4ubQdInlyu6CG0SF7bh5KOkzjQduT",
    "JOID": "Wl8cCktPCpCq7NzlPE5dwNSj6rIqKXzf9ZG1qFAvQcj4tIzeR7lsZczr3es13X2OPM_mSc6aANfb96KHgnwwY2M=",
    "osd": "VF0WAkhBCJqi79LnNkZeztap4rEkK3bX9p-3olgsT8ryvI_QRbNkZsLp1-M203-ENMzoS8SSA9nZ_aqEjH46a2A=",
    "__zse_ck": "004_3aJMB=qBlNhEq2C=7jia/J0GS9YRDImpmgUKgS2NoYoDFDQxneIskOF1pxPgKyOf5pSgqIfBzhJDeayuXic3i/XqgECIA91ESUyXhOFhBYkTGgGKevXONV=7hNop3Bvq-6Gn8Re1hNhUT1QAPuD62Nv+Hi1tT6qD66bs/pBCRKPMKpOOLIX5EveA6OF6PJy2vEogGI77My1GDnfDOcZnWD7oa8Gmj1yBjZ93OzZVDThSJPELlc+QxuzfLKe4eKjxW",
    "z_c0": "2|1:0|10:1744595249|4:z_c0|80:MS4xQTJYOVJBQUFBQUFtQUFBQVlBSlZUWjl6NTJoa1RZNGhYb0FxNlg5RU9BUjk4eE82UU1kSmdnPT0=|55fed9cbd94290e52edddba14e8b67dc7d3a70ec0866bbfd3b7d4b180412bf79",
    "BEC": "738c6d0432e7aaf738ea36855cdce904",
    "tst": "h",
    "Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49": "1744612755",
}
zhihu_request_handler = RequestHandler(headers=headers, cookies=cookies)

# -*- coding: utf-8 -*-
# Date:2025-01-23 09 58
from gne import GeneralNewsExtractor

extractor = GeneralNewsExtractor()


def get_news_content(html):
    result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])
    return result

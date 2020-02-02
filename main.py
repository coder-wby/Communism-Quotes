# -*- coding: utf-8 -*-

import json

from query.es_query import content_search, result_parser

if __name__ == '__main__':
    query_word = input("输入需要查询的词汇（多个词汇用空格隔开）: \n")
    result = result_parser(content_search(query_word))
    print(json.dumps(result, indent=4, ensure_ascii=False))

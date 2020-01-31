# -*- coding: utf-8 -*-

import json

from elasticsearch import Elasticsearch

es = Elasticsearch()

# 参考文档 https://es.xiaoleilu.com/080_Structured_Search/10_compoundfilters.html


def marxism_search(sql, index="marxism"):
    return es.search(index=index, body=sql,
                     _source_includes=["content", "title"],
                     size=20)


def content_search(word_str: str, author_name="列宁", size=20):

    word_str = word_str.strip()
    word_str = word_str.replace("  ", " ")

    sql = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "content": {
                            "query": word_str,
                            "minimum_should_match": "75%",
                            "analyzer": "ik_smart",
                        }
                    }
                },
                "filter": [
                    {"term": {"author": author_name}},
                ]
            }
        },
        "highlight": {
            "pre_tags": ["<tag1>", "<tag2>"],
            "post_tags": ["</tag1>", "</tag2>"],
            "fields": {
                "content": {}
            }
        }
    }

    return es.search(index="marxism", body=sql, size=size, _source_includes=["content", "title", "author"])


if __name__ == '__main__':
    query_word = input("输入需要查询的词汇（多个词汇用空格隔开）")
    result = content_search(query_word)
    print(json.dumps(result, indent=4, ensure_ascii=False))

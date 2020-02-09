# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

es = Elasticsearch()

# 参考文档 https://es.xiaoleilu.com/080_Structured_Search/10_compoundfilters.html


def marxism_search(sql, index="marxism"):
    return es.search(index=index, body=sql,
                     _source_includes=["content", "title"],
                     size=20)


def content_search(word_str: str, author_name=None, size=20):

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

    """ 不限定作者 """
    if author_name is None:
        del sql["query"]["bool"]["filter"]

    return es.search(index="marxism", body=sql, size=size, _source_includes=["content", "title", "author"])


def result_parser(es_result: dict) -> list:
    result_list = es_result["hits"]["hits"]
    for i in range(len(result_list)):
        del result_list[i]["_index"]
        del result_list[i]["_type"]
        del result_list[i]["_id"]
        del result_list[i]["_score"]
    return result_list

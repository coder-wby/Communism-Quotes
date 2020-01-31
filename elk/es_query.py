# -*- coding: utf-8 -*-

import json

from elasticsearch import Elasticsearch

es = Elasticsearch()

dsl_dict = {
    "query": {
        "bool": {
            "must": [
                # {"match": {"title": None}},
                {"match": {"content": "走狗"}}
            ],
            "filter": [
                {"term":  {"author": "列宁"}},
                # {"range": {"publish_date": { "gte": "2015-01-01" }}}
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

dsl_match = {
    "query": {
        "match": {
            "content": {
                "query": "美帝国主义",
                "analyzer": "ik_smart",
            },

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


def marxism_search(sql, index="marxism"):
    return es.search(index=index, body=sql,
                     _source_includes=["content", "title"],
                     size=20)


if __name__ == '__main__':
    result = marxism_search(dsl_match)
    print(json.dumps(result, indent=4, ensure_ascii=False))

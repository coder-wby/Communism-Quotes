# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, helpers

from util.html_parser import bulk_doc_json

es = Elasticsearch()

SUPPORT_AUTHOR_LIST = ["lenin-cworks", "maozedong"]
AUTHOR_NAME_DICT = {
    "lenin-cworks": "列宁",
    "maozedong": "毛泽东",
}


def create_index(_index_name='marxism'):
    """ 新建ElasticSearch的index """
    if es.indices.exists(_index_name):
        assert ValueError(f"索引{_index_name}已存在")
    return es.indices.create(index=_index_name, ignore=400)


def reset_index(_index_name='marxism'):
    """ 重置ElasticSearch的index """

    if es.indices.exists(_index_name):
        es.indices.delete(index=_index_name, ignore=[400, 404])
        print("[1] 删除原有索引")

    es.indices.create(index=_index_name, ignore=400)
    print("[2] 创建新索引")

    create_ik_mapping()
    print("[3] 配置分词引擎")


def create_ik_mapping(_index_name="marxism", _doc_type="article"):
    """ 设置ik分词的mapping
        https://github.com/medcl/elasticsearch-analysis-ik

        ik_max_word: 会将文本做最细粒度的拆分
            比如会将“中华人民共和国国歌”拆分为“中华人民共和国,中华人民,中华,华人,人民共和国,人民,人,民,共和国,共和,和,国国,国歌”，会穷尽各种可能的组合，适合 Term Query；
        ik_smart: 会做最粗粒度的拆分
            比如会将“中华人民共和国国歌”拆分为“中华人民共和国,国歌”，适合 Phrase 查询。
    """

    mapping = {
        'properties': {
            'title': {'type': 'text', 'analyzer': 'ik_max_word', 'search_analyzer': 'ik_smart'},
            'author': {'type': 'text', 'analyzer': 'ik_max_word', 'search_analyzer': 'ik_smart'},
            'content': {'type': 'text', 'analyzer': 'ik_max_word', 'search_analyzer': 'ik_smart'},
        }
    }

    return es.indices.put_mapping(index=_index_name, doc_type=_doc_type, body=mapping,
                                  include_type_name=True)


def batch_insert(author):
    """ 批量输入es文档 """

    for para_json_list in bulk_doc_json(author):
        # 批量插入
        try:
            helpers.bulk(client=es, actions=para_json_list, index="marxism", doc_type="article")
            print(f"正在插入{para_json_list[0]['title']}.")
        except Exception as e:
            print("\nERROR:", e)

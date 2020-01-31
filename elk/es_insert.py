# -*- coding: utf-8 -*-

import uuid

from elasticsearch import Elasticsearch, helpers

from util.html_parser import HTMLParser
from util.data_loader import load_origin_html_list

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


def create_ik_mapping():
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

    return es.indices.put_mapping(index='marxism', doc_type='politics', body=mapping,
                                  include_type_name=True)


def bulk_json_data(json_list, _index, doc_type):
    """ generator to push bulk data from a JSON file into an ElasticSearch index """

    for doc in json_list:
        # use a `yield` generator so that the data isn't loaded into memory
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                "_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }


def batch_insert(author):
    """ 批量输入es文档 """

    if isinstance(author, str):
        author_list = [author]
    elif isinstance(author, list):
        author_list = author
    else:
        return

    for author in author_list:

        html_parser = HTMLParser(author=author)  # 为每个作者新建一个parser
        _article_path_list = load_origin_html_list(author)  # 获得作者的所有文章地址

        for _article_path in _article_path_list:  # 逐个解析作者文章

            article_info, para_list = html_parser.parse_html_file(_article_path)
            if article_info is None or para_list is None:
                continue

            # 把每个自然段包装成一个JSON
            para_json_list = []
            for i, para in enumerate(para_list):
                para_json_list.append(article_info.copy())
                para_json_list[i]['content'] = para

            # 批量插入
            try:
                response = helpers.bulk(es, bulk_json_data(para_json_list, "marxism", "politics"))
                print(f"插入《{article_info['title']}》, 得到反馈结果 {response}.")
            except Exception as e:
                print("\nERROR:", e)


if __name__ == '__main__':
    batch_insert(["maozedong", "lenin-cworks"])
    # reset_index()
    pass

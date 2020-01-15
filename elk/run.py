# -*- coding: utf-8 -*-

import os
import uuid

from elasticsearch import Elasticsearch, helpers

from util.html_parse import parse_html_file

html_file_folder = "../material/lenin-cworks"
es = Elasticsearch()


def init():
    """ Build ElasticSearch index """
    return es.indices.create(index='marxism', ignore=400)


def reset():
    es.indices.delete(index='marxism', ignore=[400, 404])
    return es.indices.create(index='marxism', ignore=400)


def ik_setting():

    mapping = {
        'properties': {
            'full_title': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                'search_analyzer': 'ik_max_word'
            },
            'article_title': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                'search_analyzer': 'ik_max_word'
            },
            'content': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                'search_analyzer': 'ik_max_word'
            },
            'author': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                'search_analyzer': 'ik_max_word'
            },

        }
    }
    return es.indices.put_mapping(index='marxism', doc_type='politics',
                                  body=mapping,
                                  include_type_name=True)


def bulk_json_data(json_list, _index, doc_type):
    """ generator to push bulk data from a JSON
        file into an ElasticSearch index
    """
    for doc in json_list:
        # use a `yield` generator so that the data isn't loaded into memory
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                "_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }


def insert():
    vol_list = os.listdir(html_file_folder)

    # Every volume
    for vol_name in vol_list:
        vol_folder = os.path.join(html_file_folder, vol_name)

        article_list = [article for article in os.listdir(vol_folder) if article.endswith("html")]

        # For every html article
        for article_name in article_list:
            article_path = os.path.join(vol_folder, article_name)

            # Parse article
            title, sub_title, data_text, para_list = parse_html_file(article_path)

            para_json_template = {
                'full_title': title,
                'article_title': sub_title,
                'date_text': data_text,
                'date': None,
                'author': '列宁',
                'source': "列宁全集第" + vol_name + "卷",
                'content': None
            }

            para_json_list = []
            # For every paragraph
            for i, para in enumerate(para_list):
                para_json_list.append(para_json_template.copy())
                para_json_list[i]['content'] = para

            try:
                # make the bulk call, and get a response
                response = helpers.bulk(es, bulk_json_data(para_json_list, "marxism", "politics"))
                print("\nbulk_json_data() RESPONSE:", response)
            except Exception as e:
                print("\nERROR:", e)


if __name__ == '__main__':
    insert()

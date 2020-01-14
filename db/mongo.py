# -*- coding: utf-8 -*-

import os

import pymongo

from util.html_parse import parse_html_file

html_file_folder = "../material/lenin-cworks"

client = pymongo.MongoClient(host="localhost", port=27017)

marxism_cn = client.marxism_cn
article_table = marxism_cn['article']


def insert():

    vol_list = os.listdir(html_file_folder)
    print(vol_list)

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

            print(para_json_list)

            insert_result = article_table.insert_many(para_json_list)
            print(insert_result)


def query(target_word):
    results = article_table.find(filter={'content': {'$regex': target_word}},
                                 projection={"_id": 0, "date": 0, "article_title": 0, "source": 0, "author": 0})
    # sorted_results = results.sort("words_result.probability.average", pymongo.DESCENDING)
    sorted_results = results
    print(sorted_results)
    for result in sorted_results:
        print(result)


if __name__ == '__main__':
    input_key = input("输入想查询的《列宁选集》关键字（例如：修正主义）:")
    query(input_key)

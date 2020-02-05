# -*- coding: utf-8 -*-

from smoothnlp.algorithm.phrase import extract_phrase

from util.html_parser import bulk_doc_json

if __name__ == '__main__':
    doc_content_list = []
    for bulk_json in bulk_doc_json(["maozedong",]):

        for doc_json in bulk_json:
            doc_content = doc_json["content"]
            doc_content_list.append(doc_content)

    result = extract_phrase(corpus=doc_content_list, top_k=.99)
    print(result)

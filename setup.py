# -*- coding: utf-8 -*-

import os
import json

import requests
import yaml

from backend.storage.es_insert import create_index, batch_insert


def todo():

    """ 检查 config.yaml文件 """
    config_path = "conf/config.yaml"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"未找到配置文件{config_path}，请重命名并修改config-template.yaml。")

    with open("conf/config-template.yaml", "r") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    """ 检查 ElasticSearch 目录 """
    es_path = conf['elasticsearch_path']
    if es_path == "":
        raise ValueError("ElasticSearch配置信息为空，请配置ElasticSearch的bin目录。")


if __name__ == '__main__':

    """ 检查 ElasticSearch 启动情况 """
    try:
        response = requests.get("http://localhost:9200", timeout=20)
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except ConnectionRefusedError as connect_error:
        raise ConnectionRefusedError("无法连接ElasticSearch，请先运行ES。")

    """ 向ES中插入数据 """
    create_index()
    batch_insert(["maozedong", "lenin-cworks"])

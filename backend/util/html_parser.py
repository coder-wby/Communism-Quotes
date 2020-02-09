# -*- coding: utf-8 -*-

import re
import os

import yaml

from lxml import etree
from backend.util.text_parser import check_contain_chinese
from backend.util.data_loader import load_origin_html_list

""" HTML解析器
    原始数据是从马克思主义中文文库上抓取的HTML网页。
    这里需要把文本信息从HTML页面中抽取出来。
"""

gbk_parser = etree.HTMLParser(encoding='GBK')  # 原始网页是GBK编码，所以需要手动设置格式。

UTIL_ROOT = os.path.dirname(__file__)

with open(os.path.join(UTIL_ROOT, "..", "..", "conf", "author.yaml"), "r", encoding="utf-8") as f:
    author_conf = yaml.load(f, Loader=yaml.FullLoader)

AUTHOR_NAME_DICT = author_conf["author"]  # 目前支持的作者列表


class HTMLParser:

    def __init__(self, author):
        self.author = author
        self.author_name = AUTHOR_NAME_DICT[author]

        self.author_parser_dict = {
            "lenin-cworks": self._parse_lenin_cworks,
            "maozedong": self._parse_maozedong,
        }
        self.author_parser = self.author_parser_dict[author]  # 为每个作者挑选专用的parser
        self.article_info = dict()

    def _parse_lenin_cworks(self):
        """ 针对列宁全集设计的专用parse """

        # 把卷名与文章名字隔开
        try:
            """ <title>列宁全集第八卷――凡例</title> """
            vol_name, *article_name = self.article_info["title"].split("——")
            # 对于有多个破折号的标题，需要把后面的部分进行连接
            if isinstance(article_name, list):
                article_name = "——".join(article_name)
        except ValueError:
            raise print(self.article_info["title"])
        self.article_info["source"] = vol_name
        self.article_info["title"] = article_name

        # 如果HTML是凡例、目录、前言，那么就不予以采用
        if article_name in ["凡例", "目录", "前言", ]:
            return None

        return self.article_info

    def _parse_maozedong(self):
        """ 针对毛泽东文集设计的专用parse """

        """ <title>湖南农民运动考察报告（一九二七年三月）</title> """
        # 把括号都统一为中文括号
        _title_str = self.article_info["title"]
        _title_str = _title_str.replace("（", "(")
        _title_str = _title_str.replace("）", ")")
        self.article_info["title"] = _title_str

        return self.article_info

    @staticmethod
    def _parse_content(content_list):
        """ 解析文章内容 """

        result_str_list = []

        i = 0
        length = len(content_list)
        pre_content_list = []  # 保持没有正常标点结尾的句子

        while i < length:

            content = content_list[i]
            i += 1

            # 判断某句话可以删除
            if content in ["马克思主义中文文库"]:
                continue

            # 删除不带有中文字符的语段
            if not check_contain_chinese(content):
                continue

            # 判断句子是否以标点结束
            if content.endswith("。") or \
                    content.endswith("！") or \
                    content.endswith("？") or \
                    content.endswith("……"):
                # 如句子以正常的标点结束

                # 如果pre_content_list不为空，那么就把本句话作为前面所有语句的结尾。
                if pre_content_list:
                    content = "".join(pre_content_list) + content
                # 清空pre_content_list
                pre_content_list = []

            else:
                # 如句子没有以正常的标点结束，那么就把该句放入pre_content_list
                pre_content_list.append(content)
                continue

            # 删除一些特定字符
            target_list = ["\n", "\r", "\t", "\u3000", "\u2000"]
            for target in target_list:
                content = content.replace(target, "")

            """ 把经过处理的文本保存下来 """
            result_str_list.append(content)

        return result_str_list

    def parse_html_file(self, _html_file_path: str) -> (dict, list):
        """ 解析HTML文档
            :param
                _html_file_path: str, 需要解析HTML的地址
            :return:
                _article_info: dict
                _content_str_list: list
        """

        # 解析HTML文件
        _origin_html = etree.parse(_html_file_path, parser=gbk_parser)

        # 抽取关键字段
        _title_str = _origin_html.findtext('.//title')  # HTML标题
        _author_str = _origin_html.findtext('.//p[@class="author"]')  # author字段里的数据基本上是None
        _date_str = _origin_html.findtext('.//p[@class="date"]')
        _title_0_str = _origin_html.findtext('.//p[@class="title0"]')
        _title_1_str = _origin_html.findtext('.//p[@class="title1"]')
        _content_str_list = list(map(str, _origin_html.xpath("//text()")))  # 文章内容

        # 判断是否有标题信息
        if _title_str is None:
            return None, None
        else:
            _title_str = _title_str.replace(" ", "")  # 删除空格

        # 检查日期字段
        if _date_str and len(_date_str) > 64:
            _date_str = None

        # 文档信息的字段
        self.article_info = {
            'title': _title_str,
            'author': self.author_name,
            'date_text': _date_str,
            'date': None,
            'source': None,
        }

        # 每个作者采用不同的引擎
        _article_info = self.author_parser()
        # 文章内容采用相同的引擎
        _content_str_list = self._parse_content(_content_str_list)

        return _article_info, _content_str_list


def bulk_doc_json(author):
    """ 用Python生成器的方式构造json list """

    if isinstance(author, str):
        author_list = [author]
    elif isinstance(author, list):
        author_list = author
    else:
        raise ValueError("暂时不支持该作者")

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

            yield para_json_list


def parse_vol_str(_vol_str, mode='lenin-cworks'):
    """
    《列宁全集》第三十八卷
    列宁全集第三十九卷
    列宁全集第39卷
    《列宁全集》第三十九卷
    列宁全集第四十卷
    """
    if mode == 'lenin-cworks':
        book_name = "《列宁全集》"
        pattern = r'第(.*)卷'
        vol_name = re.findall(pattern, _vol_str)[0]

        return book_name + vol_name
    return


if __name__ == '__main__':
    print(AUTHOR_NAME_DICT)

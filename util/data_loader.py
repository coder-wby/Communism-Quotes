# -*- coding: utf-8 -*-

""" HTML文件列表加载器

    每个人的著作列表是不同的，所以需要为每个人设计一个接口。
"""

import os
import yaml


ROOT = os.path.dirname(__file__)  # util/
MATERIAL_ROOT = os.path.join(ROOT, "..", "material")

with open(os.path.join(ROOT, "../conf/author.yaml"), "r", encoding="utf-8") as f:
    author_conf = yaml.load(f, Loader=yaml.FullLoader)

VALID_AUTHOR_LIST = list(author_conf["author"].keys())  # 目前支持的作者列表


def load_origin_html_list(author: str) -> list:
    """ 根据作者信息 找到该作者的所有文章的HTML地址
        :param author: str, the name of author
        :return: list, the list of HTML absolute path.
    """

    assert author in VALID_AUTHOR_LIST

    """ 判断作者文献是否存在 """
    if not os.path.exists(os.path.join(MATERIAL_ROOT, author)):
        raise FileNotFoundError(f"未找到文件夹{os.path.join(MATERIAL_ROOT, author)}")

    # 作者文献的根目录
    _root_path = os.path.join(MATERIAL_ROOT, author)

    if author == 'lenin-cworks':  # 列宁全集
        _vol_str_list = [_vol_str for _vol_str in os.listdir(_root_path)]

        _html_list = []

        for _vol_str in _vol_str_list:
            _vol_root_path = os.path.join(_root_path, _vol_str)
            if not os.path.isdir(_vol_root_path):
                continue
            _html_list.extend([os.path.join(_vol_root_path, _html_str) for _html_str in os.listdir(_vol_root_path)
                               if _html_str.endswith(".html")])

        return _html_list

    if author == 'maozedong':  # 毛泽东著作

        _html_list = [os.path.join(_root_path, html_name) for html_name in os.listdir(_root_path)
                      if html_name.endswith("html")]

        return _html_list

    return []

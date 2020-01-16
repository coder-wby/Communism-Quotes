# -*- coding: utf-8 -*-

""" HTML文件列表加载器

    每个人的著作列表是不同的，所以需要为每个人设计一个接口。
"""

import os

ROOT = os.path.abspath('../material')


def load_origin_html_list(author) -> list:

    if author == 'lenin-cworks':  # 列宁全集
        _root_path = os.path.join(ROOT, author)
        _vol_str_list = [_vol_str for _vol_str in os.listdir(_root_path)]

        _html_list = []

        for _vol_str in _vol_str_list:
            _vol_root_path = os.path.join(_root_path, _vol_str)
            if not os.path.isdir(_vol_root_path):
                continue
            _html_list.extend([os.path.join(_vol_root_path, _html_str) for _html_str in os.listdir(_vol_root_path)
                               if _html_str.endswith(".html")])

        return _html_list

    return []

#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_text(doc, tag_id, value=False):
    """
    beautifulsoup get_text() wrapper
    优雅地处理 doc.find() 为 None的情况

    :param doc: beautifulsoup doc
    :param tag_id: tag id
    :param value: 是否取tag中value属性的值
    :return:
    """
    res = doc.find(id=tag_id)
    if res is not None:
        if value:
            if 'value' in res.attrs:
                return res.attrs['value']
            else:
                return ''
        else:
            return res.get_text()


def save_to_qiniu():
    """
    文件上传至七牛
    :return: url
    """
    pass

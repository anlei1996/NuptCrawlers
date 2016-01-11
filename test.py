#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from ZfCrawler import ZfCrawler

app = Flask(__name__)


zc = ZfCrawler()


@app.route('/')
def index():
    return '<img src="/captcha">', 200


@app.route('/captcha')
def captcha():
    """
    Content-Type:image/Gif; charset=gb2312
    :return:
    """
    img, cookie = zc.get_captcha()
    return img


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
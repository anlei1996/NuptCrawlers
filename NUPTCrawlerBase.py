#!/usr/bin/env python
# -*- coding: utf-8 -*-


class NUPTCrawlerBase(object):
    """
    NUPT爬虫通用类
    """
    def __init__(self, debug=False):
        self.debug = debug

    def _login(self, login_data=None, cookies=None):
        pass

    def login(self, login_data=None, cookies=None):
        return self._login(login_data=login_data, cookies=cookies)

    def get_data(self, cookies=None, student_id=None):
        pass

    def find_in_cache(self, cache_conn):
        pass

    def insert_to_db(self, db_conn):
        pass

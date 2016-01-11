#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urlparse import urlparse
from datetime import date
import json
from requests import Session

from config import Config
from NUPTCrawlerBase import NUPTCrawlerBase
from lib.util import api
from lib.http import req
from lib.PageParser import EhomeParser


class EhomeCrawler(NUPTCrawlerBase):
    def __init__(self, debug=False):
        super(EhomeCrawler, self).__init__(debug=debug)
        self.URLS = Config.EHOME_URLS
        self.host = urlparse(self.URLS['COOKIE']).netloc
        self.proxies = Config.PROXIES
        self.session = Session()
        self.session.proxies = self.proxies
        self.cookies = None
        self.iplanet = None

    def _login(self, login_data):
        resp = req(self.URLS['COOKIE'], 'get', host=self.host)
        if resp is None:
            return Config.SERVER_MSG['SERVER_ERROR']
        api.logger.info('[+] ID: %s got ehome cookies.' % login_data['number'])

        self.cookies = resp.cookies
        payload = {
            'email': login_data['student_id'],
            'password': login_data['password']
        }

        resp = req(self.URLS['LOGIN'], 'post', data=payload, cookies=self.cookies)
        # 校园系统bug 无需这一步
        # if resp.url != self.URLS['LOGIN_SUCCESS']:
        #     return Config.SERVER_MSG['WRONG_PASSWORD']
        if resp is None:
            return Config.SERVER_MSG['SERVER_ERROR']
        api.logger.info('[+] ID: %s login ehome.' % login_data['student_id'])
        self.iplanet = resp.history[0].cookies
        self.session.cookies = self.iplanet

    def _get_cardno(self):
        resp = self.session.get(self.URLS['INDEX'])
        if resp is None:
            return Config.SERVER_MSG['SERVER_ERROR']
        content = resp.text
        info = EhomeParser.parse_ehome_info(content)
        api.logger.info('[+] got cardno: %s.' % info['usercode'])
        return json.dumps(info, ensure_ascii=False)

    def _get_rec(self, start_date, usercode):
        rec = []
        fanka_data = {
            'param_0': 0,
            'param_1': 1  # 每页显示数
        }

        params = {
            'className': 'cn.com.system.query.DealQuery',
            'methodName': 'getDealQuery',
            'paramCount': '6',
            'param_2': start_date,
            'param_3': str(date.today()),
            'param_4': '-1',
            'param_5': usercode
        }
        resp = self.session.post(self.URLS['REC'], params=params, data=fanka_data)
        res = resp.json()
        total_count = int(res['totalCount'])
        api.logger.info('[+] got total_count %s of %s' % (total_count, usercode))
        if total_count > 0:
            fanka_data['param_1'] = total_count
            resp = self.session.post(self.URLS['REC'], params=params, data=fanka_data)
            if resp is None:
                return "[]"
            res = resp.json()
            rec = res['results']
        else:
            pass
        return json.dumps(rec, ensure_ascii=False)

    def get_data(self, start_date='2012-09-01', usercode=''):
        api.logger.info('[+] start fetching ehome data for %s' % usercode)
        pass

if __name__ == '__main__':
    # print str(date.today())
    ec = EhomeCrawler(debug=True)
    ec.login({'student_id': Config.TEST_STUDENT_ID, 'password': Config.TEST_EHOME_PASSWORD})
    info = ec.get_cardno()
    print ec.get_rec('2016-01-01', Config.TEST_CARDCODE)
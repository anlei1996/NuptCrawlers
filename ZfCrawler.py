#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from PIL import Image
from StringIO import StringIO
from urlparse import urlparse
import json
import gevent

from config import Config
from NUPTCrawlerBase import NUPTCrawlerBase
from lib.util import api, save_to_qiniu
from lib.http import req
from lib.PageParser import ZfParser


class ZfCrawler(NUPTCrawlerBase):
    """
    cookie是抓取验证码时候的cookie
    """

    def __init__(self, debug=False):
        super(ZfCrawler, self).__init__(debug=debug)
        self.ZF_URLS = Config.ZF_URLS
        self.host = urlparse(self.ZF_URLS['LOGIN']).netloc
        self.vs_regex = r'<input type="hidden" name="__VIEWSTATE" value="((.[^\s])*)" />'

    def get_captcha(self):
        """
        验证码暂时需要用户输入
        模拟教务处验证码获取 http://jwxt.njupt.edu.cn/CheckCode.aspx
        <img src="http://jwxt.njupt.edu.cn/CheckCode.aspx">

        TODO:
            1. 识别验证码， 参考：http://blog.rijnx.com/post/ZF-Checkcode-Verify

        :return: captcha图片流, 正方登录cookie
        """
        resp = req(self.ZF_URLS['CAPTCHA'], 'get')
        if resp is None:
            return Config.SERVER_MSG['SERVER_ERROR']
        if self.debug:
            i = Image.open(StringIO(resp.content))
            i.save('test.gif')
        return resp.content, resp.cookies

    def _get_viewstate(self, url, cookies=None):
        """
        获取表单viewstate
        """
        resp = req(url, 'get', referer=self.ZF_URLS['LOGIN'], cookies=cookies)
        if resp is None:
            return Config.SERVER_MSG['SERVER_ERROR']
        res = re.search(self.vs_regex, resp.text, re.S)
        if res is None:
            return Config.SERVER_MSG['SERVER_ERROR']
        viewstate = res.group(1)
        return viewstate

    def _login(self, login_data=None, cookies=None):
        """
        登录正方
        :param login_data:
        :param cookies:
        :return: (student_id, 登录结果)
        """
        viewstate = self._get_viewstate(self.ZF_URLS['LOGIN'])
        if viewstate == Config.SERVER_MSG['SERVER_ERROR']:
            return Config.SERVER_MSG['SERVER_ERROR']
        login_data = {
            '__VIEWSTATE': viewstate,
            'txtUserName': login_data['student_id'],
            'TextBox2': login_data['zf_password'],
            'txtSecretCode': login_data['login_captcha'],
            'RadioButtonList1': '学生',
            'Button1': '登录',
            'lbLanguange': '',
            'hidPdrs': '',
            'hidsc': ''
        }
        resp = req(self.ZF_URLS['LOGIN'], 'post', referer=self.ZF_URLS['LOGIN'], data=login_data, cookies=cookies)
        if resp is None:
            return Config.SERVER_MSG['SERVER_ERROR']
        if resp.url.startswith(self.ZF_URLS['LOGIN_SUCCESS']):
            api.logger.info('[+] ID: %s login zf successfully.' % (login_data['txtUserName']))
            msg = Config.SERVER_MSG['LOGIN_SUCCESS']
        elif self.ZF_URLS['WRONG_CAPTCHA_FINGER'] in resp.text:
            msg = Config.SERVER_MSG['WRONG_CAPTCHA']
        elif self.ZF_URLS['INVALID_CAPTCHA_FINGER'] in resp.text:
            msg = Config.SERVER_MSG['INVALID_USERNAME']
        elif self.ZF_URLS['WRONG_PASS_FINGER'] in resp.text:
            api.logger.warning('[-] ID: %s login zf failed.' % (login_data['txtUserName']))
            msg = Config.SERVER_MSG['WRONG_PASSWORD']
        else:
            msg = Config.SERVER_MSG['SERVER_ERROR']
        return login_data['txtUserName'], msg

    def _get_personal_info(self, cookies, student_id):
        """
        获取个人信息
        """
        url = ZfParser.get_zf_urls(self.ZF_URLS['INFO'], student_id)
        resp = req(url, 'get', referer=self.ZF_URLS['LOGIN'], cookies=cookies)
        if resp is None:
            api.logger.warning('[-] got %s personal info failed.' % student_id)
            return Config.SERVER_MSG['SERVER_ERROR']
        content = resp.text
        res = ZfParser.parse_zf_info(content)
        api.logger.info('[+] got %s personal info successfully.' % student_id)
        return json.dumps(res, ensure_ascii=False)

    def _get_score(self, cookies, student_id):
        """
        获取成绩信息
        """
        url = ZfParser.get_zf_urls(self.ZF_URLS['SCORE'], student_id)
        viewstate = self._get_viewstate(url, cookies=cookies)
        score_data = {
            '__VIEWSTATE': viewstate,
            'ddlXN': '',
            'ddlXQ': '',
            'Button2': '在校学习成绩查询'
        }
        resp = req(url, 'post', data=score_data, referer=self.ZF_URLS['LOGIN'], cookies=cookies, host=self.host)
        if resp is None or resp.text is None:
            api.logger.warning('[+] got %s cert score failed.' % student_id)
            return "[]"
        content = resp.text
        res = ZfParser.parse_zf_score(content)
        api.logger.info('[+] got %s score successfully.' % student_id)
        return json.dumps(res, ensure_ascii=False)

    def _get_course(self, cookies, student_id):
        """
        获取本学期课程
        """
        pass

    def _get_cert_score(self, cookies, student_id):
        """
        获取等级考试成绩信息
        """
        url = ZfParser.get_zf_urls(self.ZF_URLS['CERT_SCORE'], student_id)
        resp = req(url, 'get', cookies=cookies, referer=self.ZF_URLS['LOGIN'])
        if resp is None or resp.text is None:
            api.logger.warning('[+] got %s cert score failed.' % student_id)
            return "[]"
        content = resp.text
        res = ZfParser.parse_zf_cert_score(content)
        api.logger.info('[+] got %s cert score successfully.' % student_id)
        return json.dumps(res, ensure_ascii=False)

    def _get_thesis(self, cookies, student_id):
        """
        获取毕业论文信息
        """
        pass

    def _get_img(self, cookies, student_id):
        """
        保存个人照片
        """
        img_url = ZfParser.get_zf_urls(self.ZF_URLS['IMG'], student_id)
        resp = req(img_url, 'get', referer=self.ZF_URLS['LOGIN'], cookies=cookies, host=self.host)
        if resp is None:
            return ''
        i = Image.open(StringIO(resp.content))
        if self.debug:
            i.save(student_id+'.jpg')
        api.logger.info('[+] got %s image successfully.' % student_id)
        url = save_to_qiniu(i)
        i.close()
        return url

    def get_data(self, cookies=None, student_id=None):
        """
        并发爬取所有信息，实时返回info信息，需要把省份证后六位传给EhomeCrawler尝试登录。
        """
        api.logger.info('[*] start fetching data from zf for %s' % student_id)
        threads = []
        info_thread = gevent.spawn(self._get_personal_info, cookies, student_id)
        threads.extend([
            info_thread,
            gevent.spawn(self._get_score, cookies, student_id),
            gevent.spawn(self._get_cert_score, cookies, student_id),
            gevent.spawn(self._get_thesis, cookies, student_id),
            gevent.spawn(self._get_course, cookies, student_id)
        ])


if __name__ == '__main__':
    zc = ZfCrawler(debug=True)
    _, cookies = zc.get_captcha()
    captcha = raw_input('login captcha: ')
    login_data = dict(student_id=Config.TEST_STUDENT_ID,
                      zf_password=Config.TEST_ZF_PASSWORD,
                      login_captcha=captcha)
    sid, _ = zc.login(login_data, cookies)
    j = zc._get_personal_info(cookies, sid)
    import pprint
    pprint.pprint(j, indent=4)
    # print zc._get_cert_score(cookies, sid)
#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config:
    HUMAN_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
        'Accept-Encoding': 'gzip,deflate,sdch',
    }

    SERVER_MSG = {
        'LOGIN_SUCCESS': 0x01,
        'INVALID_USERNAME': 0x02,
        'WRONG_PASSWORD': 0x03,
        'WRONG_CAPTCHA': 0x04,
        'SERVER_ERROR': 0x05
    }

    ZF_URLS = {
        'CAPTCHA': 'http://jwxt.njupt.edu.cn/CheckCode.aspx',
        'LOGIN': 'http://jwxt.njupt.edu.cn/',
        'LOGIN_SUCCESS': 'http://jwxt.njupt.edu.cn/xs_main.aspx',
        'INFO': 'http://jwxt.njupt.edu.cn/xsgrxx.aspx',
        'IMG': 'http://jwxt.njupt.edu.cn/readimagexs.aspx',
        'SCORE': 'http://jwxt.njupt.edu.cn/xscj_gc.aspx',
        'CERT_SCORE': 'http://jwxt.njupt.edu.cn/xsdjkscx.aspx',
        'COURSE': 'http://jwxt.njupt.edu.cn/xskbcx.aspx',
        'WRONG_CAPTCHA_FINGER': u'验证码不正确！！',
        'INVALID_CAPTCHA_FINGER': u'用户名不存在或未按照要求参加教学活动',
        'WRONG_PASS_FINGER': u'密码错误！！',
    }

    ZF_MSGS = {
        'WRONG_CAPTCHA_FINGER': u'验证码不正确！！',
        'INVALID_CAPTCHA_FINGER': u'用户名不存在或未按照要求参加教学活动',
        'WRONG_PASS_FINGER': u'密码错误！！',
    }

    LIB_URLS = {
        'CAPTCHA': 'http://202.119.228.6:8080/reader/captcha.php',
        'LOGIN': 'http://202.119.228.6:8080/reader/redr_verify.php',
        'LOGIN_SUCCESS': 'http://202.119.228.6:8080/reader/redr_info.php',
        'INFO': 'http://202.119.228.6:8080/reader/redr_info_rule.php',
        'CURRENT': 'http://202.119.228.6:8080/reader/book_lst.php',
        'HISTORY': 'http://202.119.228.6:8080/reader/book_hist.php',
        'RECOMMEND': 'http://202.119.228.6:8080/reader/asord_lst.php',
        'RESERVE': 'http://202.119.228.6:8080/reader/preg.php',
        'BOOKSHELF': 'http://202.119.228.6:8080/reader/book_shelf.php',
        'LOSS': 'http://202.119.228.6:8080/reader/book_loss.php',
        'FINE': 'http://202.119.228.6:8080/reader/account.php',
        'FINE_DETAIL': 'http://202.119.228.6:8080/reader/fine_pec.php',
        'COMMENT': 'http://202.119.228.6:8080/reader/book_rv.php',
        'SEARCH': 'http://202.119.228.6:8080/reader/search_hist.php',
        'WRONG_PASS_FINGER': u'密码错误',
        'WRONG_CAPTCHA_FINGER': 'wrong check code'
    }

    EHOME_URLS = {
        'COOKIE': 'http://my.njupt.edu.cn/ccs/main/loginIndex.do',
        'LOGIN': 'http://my.njupt.edu.cn/ccs/main.login.do',
        'LOGIN_SUCCESS': 'http://my.njupt.edu.cn/ccs/ehome/index.do',
        'INDEX': 'http://xykadmin.njupt.edu.cn/webekt/main.jsp',
        'REC': 'http://xykadmin.njupt.edu.cn/webekt/SystemListener',
    }

    TEXT_SEPARATOR = '__NUPTSPIDER_TEXT_SEPARATOR__'

    PROXIES = {
    }

    TEST_STUDENT_ID = ''
    TEST_EHOME_PASSWORD = ''
    TEST_CARDCODE = ''
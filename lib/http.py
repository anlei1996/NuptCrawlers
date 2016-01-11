#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import grequests
from copy import deepcopy
from config import Config
from lib.util import api


def req(url, method, **kwargs):
    headers = deepcopy(Config.HUMAN_HEADERS)
    if 'referer' in kwargs:
        headers.update({'Referer': kwargs['referer']})
        del kwargs['referer']
    if 'host' in kwargs:
        headers.update({'Host': kwargs['host']})
        del kwargs['host']
    kwargs.update({'headers': headers})
    try:
        kwargs.update({"timeout": (10, 10), "verify": False})
        resp = getattr(requests, method)(url, **kwargs)
    except Exception as e:
        api.logger.error("[-] url: %s, error: %s" % (url, str(e)))
        return None
    return resp

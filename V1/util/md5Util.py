# -*- coding: utf-8 -*-
__author__ = 'smilemilk'
import hashlib
def getMd5(data):
    md5=hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
    return md5


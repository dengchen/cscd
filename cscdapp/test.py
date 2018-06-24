# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
# Create your tests here.
from django.shortcuts import render,redirect,render_to_response,HttpResponse
import os, django,json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cscd.settings")
django.setup()
def hello():

    #infile = open('./data/data.json','r')
    # data = json.load(infile)
    # res = json.dumps(data).decode('unicode_escape')
    # print res
    # for i in data:
    #     print i
    '''
    方法一
    '''
    a = { "factorCode": "BOND_TYPE",
  "factorName": "债项类型",
  "options": [
    {"id":10000000001836, "name":"国债", "ratio":1.05},
    {"id":10000000001837, "name":"金融债 - 国际开发机构人民币债券、政策性银行金融债券", "ratio":1.05},
    {"id":10000000001838, "name":"金融债 - 商业银行金融债券、其他金融机构债券", "ratio":1},
    {"id":10000000001839, "name":"地方政府债券", "ratio":0.95},
    {"id":10000000001840, "name":"企业债 - 一般企业债", "ratio":0.95},
    {"id":10000000001841, "name":"公司债 - 一般公司债、可交换公司债券、可转债、资产支持证券", "ratio":0.95}
  ]
}
    result = [(item.get('name')) for item in a['options']]

    data = str(result).replace('u\'', '\'')
    b = data.decode('unicode_escape')
    print b
if __name__ == '__main__':
    hello()
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
# Create your tests here.
from django.shortcuts import render,redirect,render_to_response,HttpResponse
import os, django,json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cscd.settings")
django.setup()
def hello():

    #infile = open('./hi/hi.json','r')
    # hi = json.load(infile)
    # res = json.dumps(hi).decode('unicode_escape')
    # print res
    # for i in hi:
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



#
#     print result
#     data = str(result).replace('u\'', '\'')
#     b = data.decode('unicode_escape')
#     print b
    list1 = ['国债', '金融债 - 国际开发机构人民币债券、政策性银行金融债券', '金融债 - 商业银行金融债券、其他金融机构债券', '地方政府债券', '企业债 - 一般企业债', '公司债 - 一般公司债、可交换公司债券、可转债、资产支持证券']
    list2 =[1.05, 1.05, 1, 0.95, 0.95, 0.95]
    list = []

def Single_people1(request):
    if request.method == "GET":
        return render(request, 'Single_people1.html')
    elif request.method == "POST":
        v = request.POST.getlist('Company_nature')
        EAD = float(v[0])
        Company_nature_value = list(Company_nature.objects.filter(Type=v[1]).values_list('Coefficient', flat=True))
        Issuer_industry_value = list(Issuer_industry.objects.filter(Type=v[2]).values_list('Coefficient', flat=True))
        Credit_environment_value = list(Credit_environment.objects.filter(Type=v[3]).values_list('Coefficient', flat=True))
        Bond_type_value = list(Bond_type.objects.filter(Type=v[4]).values_list('Coefficient', flat=True))
        # 计算方法
        # 债务人调整系数
        # print Company_nature_value[0],Credit_environment_value[0],Issuer_industry_value[0]
        Debtor_coefficient = Company_nature_value[0] * Credit_environment_value[0] * Issuer_industry_value[0]
        print '债务人调整系数:', Debtor_coefficient

        # 债项特征调整系数
        # print Bond_type_value[0]
        Bond_coefficient = Bond_type_value[0]
        print  '债项特征调整系数:', Bond_coefficient

        # 抵质押品有效缓释值
        # print Collateral_type_value[0],Collateral_control_value[0],Collateral_depend_value[0],Collateral_environment_value[0]
        Collateral_coefficient = 0
        print  '抵质押品有效缓释值:', Collateral_coefficient

        # 担保人有效缓释值
        # print Guarantee_money,Guarantor_type_value[0],Guarantee_strength_value[0],Guarantee_type_value[0]
        Guarantor__coefficient = 0
        print '担保人有效缓释值:', Guarantor__coefficient

        # 原始的基础回收率
        if Collateral_coefficient + Guarantor__coefficient > 1.05:
            OriginalRecycling_value = (Collateral_coefficient + Guarantor__coefficient) / EAD
            print '原始的基础回收率:', OriginalRecycling_value
        else:
            OriginalRecycling_value = 0.35
            print '原始的基础回收率:', OriginalRecycling_value

        # 基础回收率
        if OriginalRecycling_value < 1.05:
            BasisRecycling_value = OriginalRecycling_value
            print '基础回收率：', BasisRecycling_value
        else:
            BasisRecycling_value = 1.05
            print '基础回收率：', BasisRecycling_value
        # LGD值
        LGD_value = 1 - BasisRecycling_value * Bond_coefficient * Debtor_coefficient
        print 'LGD值：',LGD_value

        # lGD级别

        if LGD_value >= -99999 and LGD_value < 0.01:

            LGD_level = "LGD1"
        elif LGD_value >= 0.01 and LGD_value < 0.1:
            LGD_level = 'LGD2'
        elif LGD_value > 0.1 and LGD_value < 0.3:
            LGD_level = 'LGD3'
        elif LGD_value >= 0.3 and LGD_value < 0.4:
            LGD_level = 'LGD4'
        elif LGD_value >= 0.4 and LGD_value < 0.5:
            LGD_level = 'LGD5'
        elif LGD_value >= 0.5 and LGD_value < 0.6:
            LGD_level = 'LGD6'
        elif LGD_value >= 0.6 and LGD_value < 0.7:
            LGD_level = 'LGD7'
        elif LGD_value >= 0.7 and LGD_value < 0.8:
            LGD_level = 'LGD8'
        elif LGD_value >= 0.8 and LGD_value < 0.9:
            LGD_level = 'LGD9'
        elif LGD_value >= 0.9 and LGD_value <= 1:
            LGD_level = 'LGD10'
        else:
            LGD_level = '级别太高啦，找不到！'
        print 'LGD级别：', LGD_level

        list_value = [Debtor_coefficient, Bond_coefficient, Collateral_coefficient, Guarantor__coefficient, OriginalRecycling_value
        , BasisRecycling_value, LGD_value,LGD_level]
        dict_value = {}
        dict_value['json_str'] = list_value
        json_str = json.dumps(dict_value)
        return HttpResponse(json_str)
    else:
        # PUT,DELETE,HEAD,OPTION...
        return redirect('/Single_people1/')
def test():
#     data_values =[]
#     data =[]
#     list = [u'', u'1.05', u'1.1', u'1.05', u'1.05', u'A1', u'', u'1.0', u'0.7', u'1.0', u'1.0', u'', u'1', u'1', u'1', u'A1']
#     for i in list:
#         v = str(i).replace('u\'', '\'').encode('utf-8')
#         data.append(v)
#     print data
#     print type(data)
#     a = float(data[5])
#     print a
#


    #     b = data.decode('unicode_escape')
    a =[
      {
        "id": 1,
        "rating": "A1",
        "type": "无级别",
        "midPd": 1.179e-5,
        "maxValue": 2.035e-5,
        "minValue": 0.0,
        "creationTime": "2016-11-08T00:00",
        "clientId": 1,
        "isDelete": 0
      },
      {
        "id": 2,
        "rating": "A2",
        "type": "无级别",
        "midPd": 3.512e-5,
        "maxValue": 6.061e-5,
        "minValue": 2.035e-5,
        "creationTime": "2016-11-08T00:00",
        "clientId": 1,
        "isDelete": 0
      }
    ]

def LGD():
    LGDValue =0.25
    a =  [
  { "lgdId": 1, "level": "LGD1", "upperBound": 0.1, "midPoint": 0.05, "lowBound": -99999.0, "adjust": 2},
  { "lgdId": 2, "level": "LGD2", "upperBound": 0.2, "midPoint": 0.15, "lowBound": 0.1, "adjust": 1 },
  {"lgdId": 2, "level": "LGD3", "upperBound": 0.3, "midPoint": 0.25, "lowBound": 0.2, "adjust": 1},
            ]
    for i in range(len(a)):
        item = a[i]
        if item['lowBound']<LGDValue and item['upperBound']>=LGDValue:
            level = item['level']
            break
    print level

def fun():

    a= 1+1
    print a
def fun1():
    b = fun()
    print b
if __name__ == '__main__':
    hello()
    #test()
    #LGD()
    fun1()
# -*- coding: utf-8 -*-
'''
1.LGD级别-----通过LGD值映射表
2.LGD值=1-基础回收率（上限1.05）*债务人特征调整系数*债项特征调整系数 LGD_value
3.基础回收率（上限1.05）:如果【原始的基础回收率】小于1.05那么就等于原始的基础回收率，否则就等于1.05  BasisRecycling_value
4.原始的基础回收率:担保人缓释价值+抵质押品缓释价值大于0，那么就等于(担保人缓释价值+抵质押品缓释价值)/债券风险暴露EAD,否则就等于0.35 OriginalRecycling_value
5.担保人缓释价值=抵质押品价值*抵质押品类型*抵质押品控制力*抵质押品执法环境 Guarantor__coefficient
6.抵质押品缓释价值=担保人类型*担保强度*担保价值*担保类型 Collateral_coefficient
7债务人特征调整系数=股权结构*发行人行业*信用环境 Debtor_coefficient
8债项特征调整系数:等于债项类型 Bond_coefficient
'''
from __future__ import unicode_literals
import os, django,json
from django.shortcuts import render,redirect,render_to_response,HttpResponse
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cscd.settings")
django.setup()
from cscdapp import models
from django.forms import ModelChoiceField
# Create your views here.
'''
      bondFeatureAdjustCoefficient    债项特征调整系数
      debtorFeatureAdjustCoefficient  债务人特征调整系数
      pledgeReleasePrice  抵质押品缓释价值
      warrantorReleasePrice 担保人缓释价值
      originalBasisRecoveryRate  原始的基础回收率
      basisRecoveryRate  基础回收率
      LGDValue  LGD值
      LGDLevel  LGD级别
      companyBasisRating   债券基础评级
      guaranterRating    担保人有效评级
      finallyRating   最终评级
      bondBalance   债券余额
      bondType  债项类型
      companyNature 股权结构
      industary 发行人行业
      creditRegion  信用环境
      warrantorType 担保人类型
      warrantyStrength  担保强度
      guaranteeType 担保类型
      pledgeType    抵质押品类型
      pledgeControl 抵质押品控制力
      pledgeRegion  抵质押品执法环境
      pledgeDepend  抵质押物独立性
      companyRating 发行人有效认定评级
      warrantorRating 担保人有效认定评级
'''
def test(request):
    secrets = open("cscdapp\\static\\data.json",'r')
    data = json.load(secrets)
    if request.method == "GET":
        return render(request,'test.html',{"bondType":data[0]["options"],"bondType_factorName":data[0]['factorName'],
                                           "companyNature":data[1]["options"],"companyNature_factorName":data[1]['factorName'],
                                           "creditRegion":data[2]["options"],"creditRegion_factorName":data[2]['factorName'],
                                           "industary":data[3]["options"],"industary_factorName":data[3]['factorName'],
                                           "guaranteeType":data[4]["options"],"guaranteeType_factorName":data[4]['factorName'],
                                           "warrantorType":data[5]["options"],"warrantorType_factorName":data[5]['factorName'],
                                           "warrantyStrength":data[6]["options"],"warrantyStrength_factorName":data[6]['factorName'],
                                           "pledgeControl":data[7]["options"],"pledgeControl_factorName":data[7]['factorName'],
                                           "pledgeDepend":data[8]["options"],"pledgeDepend_factorName":data[8]['factorName'],
                                           "pledgeRegion":data[9]["options"],"pledgeRegion_factorName":data[9]['factorName'],
                                           "pledgeType":data[10]["options"],"pledgeType_factorName":data[10]['factorName'],
                                           "companyRating":data[12],
                                           "warrantorRating":data[12],
                                           },)
    elif request.method == "POST":
        request_values = request.POST.getlist('Company_nature') #获取提交数据 unicode类型

        #unicode类型转list类型


        '''
        计算结果
        '''
        #债项特征调整系数:等于债项类型
        bondFeatureAdjustCoefficient = request_values[1]
        print '债项特征调整系数：',bondFeatureAdjustCoefficient

        #债务人特征调整系数 = 股权结构 * 发行人行业 * 信用环境
        debtorFeatureAdjustCoefficient = float(request_values[2])*float(request_values[3])*float(request_values[4])
        print '债务人特征调整系数：',debtorFeatureAdjustCoefficient

        #抵质押品缓释价值=抵质押品价值*抵质押品类型*抵质押品控制力*抵质押品执法环境
        pledgeReleasePrice = float(request_values[6])*float(request_values[7])*float(request_values[8])*float(request_values[9])
        print '抵质押品缓释价值：',pledgeReleasePrice

        #担保人缓释价值=担保人类型*担保强度*担保价值*担保类型
        warrantorReleasePrice = float(request_values[10])*float(request_values[11])*float(request_values[12])*float(request_values[13])
        print '担保人缓释价值：',warrantorReleasePrice


        #原始的基础回收率:担保人缓释价值+抵质押品缓释价值大于0，那么就等于(担保人缓释价值+抵质押品缓释价值)/债券风险暴露EAD,否则就等于0.35
        if pledgeReleasePrice+warrantorReleasePrice >0:
            originalBasisRecoveryRate = (pledgeReleasePrice+warrantorReleasePrice)/float(request_values[0])
            print '原始的基础回收率：',originalBasisRecoveryRate
        else:
            originalBasisRecoveryRate = 0.35
            print '原始的基础回收率：',originalBasisRecoveryRate


        list_value = [bondFeatureAdjustCoefficient]
        dict_value = {}
        dict_value['json_str'] = list_value
        json_str = json.dumps(dict_value)
        print json_str
        return HttpResponse(json_str)
    else:
        return render(request, 'test.html')







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
from cscdapp.form import noPledgeGuarantee,noPledgeOneGuarantee,onePledgeNoGuarantee,onePledgeOneGuarantee
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
      bondBasisRating   债券基础评级
      guaranterRating    担保人有效评级
      finallyRating   最终评级
      bondBalance   债券余额
      
      bondType  债项类型
      companyNature 股权结构
      industary 发行人行业
      creditRegion  信用环境
      
      warrantorType 担保人类型
      warrantyMoney 担保金额
      warrantyStrength  担保强度
      guaranteeType 担保类型
      
      pledgeMoney 抵押金额
      pledgeType    抵质押品类型
      pledgeControl 抵质押品控制力
      pledgeRegion  抵质押品执法环境
      pledgeDepend  抵质押物独立性
      
      companyRating 发行人有效认定评级
      warrantorRating 担保人有效认定评级
'''
def function_debtorFeatureAdjustCoefficient(a,b,c): #债务人特征调整系数 = 股权结构 * 发行人行业 * 信用环境
    return float(a)*float(b)*float(c)

def function_pledgeReleasePrice(a,b,c,d,e):#抵质押品缓释价值=抵质押品价值*抵质押品类型*抵质押品控制力*抵质押品执法环境
    return float(a) * float(b) * float(c) * float(d) * float(e)

def function_warrantorReleasePrice(a,b,c,d):#担保人缓释价值=担保人类型*担保强度*担保价值*担保类型
    return float(a) * float(b) * float(c)*float(d)

def funciton_originalBasisRecoveryRate(a,b,c):#原始的基础回收率:担保人缓释价值+抵质押品缓释价值大于0，# 那么就等于(担保人缓释价值+抵质押品缓释价值)/债券风险暴露EAD,否则就等于0.35
    if a + b > 0:
        return (a + b) / float(c)

    else:
        return 0.35

def function_basisRecoveryRate(a):#基础回收率（上限1.05）:如果【原始的基础回收率】小于1.05那么就等于原始的基础回收率，否则就等于1.05
    if a < 1.05:
        return  a
    else:
        return  1.05

def function_LGDLevel(a,b):
    for i in range(len(a)):
        item = a[i]
        if item['lowBound'] < b and item['upperBound'] >= b:
            return item['level']
            break

def function_bondBasisRating(a,b,c):# a = LGDLevel  b = data[12]  c = click_value 根据LDG值上升或者下调
    if a == 'LGD1' and c >= 3:
        return b[c - 2]['rating']
    elif a == 'LGD1' and c == 2:
        return b[c - 1]['rating']
    elif a == 'LGD1' and c == 1:
        return b[c]['rating']
    elif a == 'LGD2' and c >= 2:
        return b[c - 1]['rating']
    elif a == 'LGD2' and c == 1:
        return b[c]['rating']
    else:
        return b[c]['rating']

# def function_finallyRating(a,b):

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

    if request.method == "POST":
        if float(request.POST.get('select'))==0: #无抵押无担保场景
            f = noPledgeGuarantee(request.POST)
            f.is_valid()
            form_data = f.cleaned_data  # 返回字典 values为unicode
            print form_data
            bondFeatureAdjustCoefficient = float(form_data['bondType'])
            print '债项特征调整系数：',bondFeatureAdjustCoefficient
            debtorFeatureAdjustCoefficient = function_debtorFeatureAdjustCoefficient(form_data["companyNature"],form_data["industary"],form_data["creditRegion"])
            print '债务人特征调整系数：',debtorFeatureAdjustCoefficient
            pledgeReleasePrice = 0
            print '抵质押品缓释价值：',pledgeReleasePrice
            warrantorReleasePrice = 0
            print '担保人缓释价值：',warrantorReleasePrice
            originalBasisRecoveryRate = funciton_originalBasisRecoveryRate(warrantorReleasePrice,pledgeReleasePrice,form_data["bondBalance"])
            basisRecoveryRate =function_basisRecoveryRate(originalBasisRecoveryRate)
            LGDValue = 1-basisRecoveryRate*debtorFeatureAdjustCoefficient*bondFeatureAdjustCoefficient
            print "LGD值：",LGDValue
            LGDLevel = function_LGDLevel(data[11],LGDValue)
            print 'LGD级别：',LGDLevel
            company_click_value = int(float(form_data["companyRating"]))
            companyRating = data[12][company_click_value]['rating']
            print '发行人认定评级：',companyRating
            bondBasisRating = function_bondBasisRating(LGDLevel,data[12],company_click_value)
            print "债券基础评级：",bondBasisRating
            guaranterRating = '无'
            finallyRating = bondBasisRating
            print '债券最终评级：',finallyRating
            list_value = [bondFeatureAdjustCoefficient,debtorFeatureAdjustCoefficient,pledgeReleasePrice
                          ,warrantorReleasePrice,originalBasisRecoveryRate,basisRecoveryRate,LGDValue,
                          LGDLevel,companyRating,bondBasisRating,guaranterRating,finallyRating]
            dict_value = {}
            dict_value['json_str'] = list_value
            json_str = json.dumps(dict_value)
            print json_str
            return HttpResponse(json_str)
        if float(request.POST.get('select'))==1: #无抵押单担保场景
            f = noPledgeOneGuarantee(request.POST)
            f.is_valid()
            form_data = f.cleaned_data  # 返回字典 values为unicode
            bondFeatureAdjustCoefficient = float(form_data['bondType'])
            print '债项特征调整系数：',bondFeatureAdjustCoefficient
            debtorFeatureAdjustCoefficient = function_debtorFeatureAdjustCoefficient(form_data["companyNature"],form_data["industary"],form_data["creditRegion"])
            print '债务人特征调整系数：',debtorFeatureAdjustCoefficient
            pledgeReleasePrice = 0
            print '抵质押品缓释价值：',pledgeReleasePrice
            warrantorReleasePrice = function_warrantorReleasePrice(form_data['warrantyMoney'],form_data['guaranteeType'],form_data['warrantyStrength'],form_data['warrantorType'])
            print '担保人缓释价值：',warrantorReleasePrice
            originalBasisRecoveryRate = funciton_originalBasisRecoveryRate(warrantorReleasePrice,pledgeReleasePrice,form_data["bondBalance"])
            basisRecoveryRate =function_basisRecoveryRate(originalBasisRecoveryRate)
            LGDValue = 1-basisRecoveryRate*debtorFeatureAdjustCoefficient*bondFeatureAdjustCoefficient
            print "LGD值：",LGDValue
            LGDLevel = function_LGDLevel(data[11],LGDValue)
            print 'LGD级别：',LGDLevel
            company_click_value = int(float(form_data["companyRating"]))
            companyRating = data[12][company_click_value]['rating']
            print '发行人认定评级：',companyRating
            bondBasisRating = function_bondBasisRating(LGDLevel,data[12],company_click_value)
            print "债券基础评级：",bondBasisRating
            guaranter_click_value = int(float(form_data["warrantorRating"]))
            guaranterRating = data[12][guaranter_click_value]['rating']
            print "担保人有效评级：",guaranterRating
            if company_click_value <= guaranter_click_value:
                finallyRating = bondBasisRating
            else:
                finallyRating = guaranterRating
            print '债券最终评级：',finallyRating
            list_value = [bondFeatureAdjustCoefficient,debtorFeatureAdjustCoefficient,pledgeReleasePrice
                          ,warrantorReleasePrice,originalBasisRecoveryRate,basisRecoveryRate,LGDValue,
                          LGDLevel,companyRating,bondBasisRating,guaranterRating,finallyRating]
            dict_value = {}
            dict_value['json_str'] = list_value
            json_str = json.dumps(dict_value)
            print json_str
            return HttpResponse(json_str)
        if float(request.POST.get('select'))==2: #单抵押无担保场景
            f = onePledgeNoGuarantee(request.POST)
            f.is_valid()
            form_data = f.cleaned_data  # 返回字典 values为unicode
            print form_data
            bondFeatureAdjustCoefficient = float(form_data['bondType'])
            print '债项特征调整系数：',bondFeatureAdjustCoefficient
            debtorFeatureAdjustCoefficient = function_debtorFeatureAdjustCoefficient(form_data["companyNature"],form_data["industary"],form_data["creditRegion"])
            print '债务人特征调整系数：',debtorFeatureAdjustCoefficient
            pledgeReleasePrice = function_pledgeReleasePrice(form_data['pledgeMoney'],form_data['pledgeControl'],form_data['pledgeRegion'],form_data['pledgeDepend'],form_data['pledgeType'],)
            print '抵质押品缓释价值：',pledgeReleasePrice
            warrantorReleasePrice = 0
            print '担保人缓释价值：',warrantorReleasePrice
            originalBasisRecoveryRate = funciton_originalBasisRecoveryRate(warrantorReleasePrice,pledgeReleasePrice,form_data["bondBalance"])
            basisRecoveryRate =function_basisRecoveryRate(originalBasisRecoveryRate)
            LGDValue = 1-basisRecoveryRate*debtorFeatureAdjustCoefficient*bondFeatureAdjustCoefficient
            print "LGD值：",LGDValue
            LGDLevel = function_LGDLevel(data[11],LGDValue)
            print 'LGD级别：',LGDLevel
            company_click_value = int(float(form_data["companyRating"]))
            companyRating = data[12][company_click_value]['rating']
            print '发行人认定评级：',companyRating
            bondBasisRating = function_bondBasisRating(LGDLevel,data[12],company_click_value)
            print "债券基础评级：",bondBasisRating
            guaranterRating = '无'
            finallyRating = bondBasisRating
            print '债券最终评级：',finallyRating
            list_value = [bondFeatureAdjustCoefficient,debtorFeatureAdjustCoefficient,pledgeReleasePrice
                          ,warrantorReleasePrice,originalBasisRecoveryRate,basisRecoveryRate,LGDValue,
                          LGDLevel,companyRating,bondBasisRating,guaranterRating,finallyRating]
            dict_value = {}
            dict_value['json_str'] = list_value
            json_str = json.dumps(dict_value)
            print json_str
            return HttpResponse(json_str)
        if float(request.POST.get('select'))==3: #单抵押单担保场景
            f = onePledgeOneGuarantee(request.POST)
            f.is_valid()
            form_data = f.cleaned_data  # 返回字典 values为unicode
            print form_data
            bondFeatureAdjustCoefficient = float(form_data['bondType'])
            print '债项特征调整系数：',bondFeatureAdjustCoefficient
            debtorFeatureAdjustCoefficient = function_debtorFeatureAdjustCoefficient(form_data["companyNature"],form_data["industary"],form_data["creditRegion"])
            print '债务人特征调整系数：',debtorFeatureAdjustCoefficient
            pledgeReleasePrice = function_pledgeReleasePrice(form_data['pledgeMoney'],form_data['pledgeControl'],form_data['pledgeRegion'],form_data['pledgeDepend'],form_data['pledgeType'],)
            print '抵质押品缓释价值：',pledgeReleasePrice
            warrantorReleasePrice = function_warrantorReleasePrice(form_data['warrantyMoney'],form_data['guaranteeType'],form_data['warrantyStrength'],form_data['warrantorType'])
            print '担保人缓释价值：',warrantorReleasePrice
            originalBasisRecoveryRate = funciton_originalBasisRecoveryRate(warrantorReleasePrice,pledgeReleasePrice,form_data["bondBalance"])
            basisRecoveryRate =function_basisRecoveryRate(originalBasisRecoveryRate)
            LGDValue = 1-basisRecoveryRate*debtorFeatureAdjustCoefficient*bondFeatureAdjustCoefficient
            print "LGD值：",LGDValue
            LGDLevel = function_LGDLevel(data[11],LGDValue)
            print 'LGD级别：',LGDLevel
            company_click_value = int(float(form_data["companyRating"]))
            companyRating = data[12][company_click_value]['rating']
            print '发行人认定评级：',companyRating
            bondBasisRating = function_bondBasisRating(LGDLevel,data[12],company_click_value)
            print "债券基础评级：",bondBasisRating
            guaranter_click_value = int(float(form_data["warrantorRating"]))
            guaranterRating = data[12][guaranter_click_value]['rating']
            if company_click_value <= guaranter_click_value:
                finallyRating = bondBasisRating
            else:
                finallyRating = guaranterRating
            print '债券最终评级：',finallyRating
            list_value = [bondFeatureAdjustCoefficient,debtorFeatureAdjustCoefficient,pledgeReleasePrice
                          ,warrantorReleasePrice,originalBasisRecoveryRate,basisRecoveryRate,LGDValue,
                          LGDLevel,companyRating,bondBasisRating,guaranterRating,finallyRating]
            dict_value = {}
            dict_value['json_str'] = list_value
            json_str = json.dumps(dict_value)
            print json_str
            return HttpResponse(json_str)










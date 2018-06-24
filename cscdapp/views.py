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
from cscdapp.models import Company_nature,Issuer_industry,Credit_environment,Bond_type,Guarantor_type,Guarantee_type,Guarantee_strength,Collateral_depend\
    ,Collateral_type,Collateral_control,Collateral_environment,Bond_rating_scale_lgd
from django.forms import ModelChoiceField
# Create your views here.
#加载页面
def Index(request):
    return render_to_response("index.html")
#场景一：单发行人无抵押无担保场景
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

#场景二：单发行人单抵押无担保
def Single_people2(request):
    if request.method == "GET":
        return render(request, 'Single_people2.html')
    elif request.method == "POST":
        v = request.POST.getlist('Company_nature')
        EAD = float(v[0])
        Company_nature_value = list(Company_nature.objects.filter(Type=v[1]).values_list('Coefficient', flat=True))
        Issuer_industry_value = list(Issuer_industry.objects.filter(Type=v[2]).values_list('Coefficient', flat=True))
        Credit_environment_value = list(Credit_environment.objects.filter(Type=v[3]).values_list('Coefficient', flat=True))
        Bond_type_value = list(Bond_type.objects.filter(Type=v[4]).values_list('Coefficient', flat=True))
        Collateral_money = float(v[5])
        Collateral_depend_value = list(Collateral_depend.objects.filter(Type=v[6]).values_list('Coefficient', flat=True))
        Collateral_type_value = list(Collateral_type.objects.filter(Type=v[7]).values_list('Coefficient', flat=True))
        Collateral_control_value = list(Collateral_control.objects.filter(Type=v[8]).values_list('Coefficient', flat=True))
        Collateral_environment_value = list(Collateral_environment.objects.filter(Type=v[9]).values_list('Coefficient', flat=True))

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
        Collateral_coefficient = Collateral_money * Collateral_type_value[0] * Collateral_control_value[0] * \
                                 Collateral_depend_value[0] * Collateral_environment_value[0]
        print  '抵质押品有效缓释值:', Collateral_coefficient

        # 担保人有效缓释值
        # print Guarantee_money,Guarantor_type_value[0],Guarantee_strength_value[0],Guarantee_type_value[0]
        Guarantor__coefficient =0
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
        print 'LGD值：', LGD_value

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

        '''
        返回json字符串
        '''
        list_value = [Debtor_coefficient, Bond_coefficient, Collateral_coefficient, Guarantor__coefficient,
                      OriginalRecycling_value
            , BasisRecycling_value, LGD_value,LGD_level]
        dict_value = {}
        dict_value['json_str'] = list_value
        json_str = json.dumps(dict_value)
        return HttpResponse(json_str)

    else:
        # PUT,DELETE,HEAD,OPTION...
        return redirect('/Single_people2.html/')

#场景三：单发行人无抵质押单担保
def Single_people3(request):
    if request.method == "GET":
        return render(request, 'Single_people3.html')
    elif request.method == "POST":
        v = request.POST.getlist('Company_nature')
        EAD = float(v[0])
        Company_nature_value = list(Company_nature.objects.filter(Type=v[1]).values_list('Coefficient', flat=True))
        Issuer_industry_value= list(Issuer_industry.objects.filter(Type=v[2]).values_list('Coefficient', flat=True))
        Credit_environment_value= list(Credit_environment.objects.filter(Type=v[3]).values_list('Coefficient', flat=True))
        Bond_type_value= list(Bond_type.objects.filter(Type=v[4]).values_list('Coefficient', flat=True))
        Guarantee_money = float(v[5])
        Guarantor_type_value = list(Guarantor_type.objects.filter(Type=v[6]).values_list('Coefficient', flat=True))
        Guarantee_type_value = list(Guarantee_type.objects.filter(Type=v[7]).values_list('Coefficient', flat=True))
        Guarantee_strength_value = list(
        Guarantee_strength.objects.filter(Type=v[8]).values_list('Coefficient', flat=True))
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
        Guarantor__coefficient = Guarantee_money * Guarantor_type_value[0] * Guarantee_strength_value[0] * \
                                 Guarantee_type_value[0]
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
        print 'LGD值：', LGD_value

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

        '''
        返回json字符串
        '''
        list_value = [Debtor_coefficient, Bond_coefficient, Collateral_coefficient, Guarantor__coefficient,
                      OriginalRecycling_value
            , BasisRecycling_value, LGD_value,LGD_level]
        dict_value = {}
        dict_value['json_str'] = list_value
        json_str = json.dumps(dict_value)
        return HttpResponse(json_str)
    else:
        redirect('/Single_people3.html/')

#场景四：单发行人单抵押单担保
def Single_people4(request):
    if request.method == "GET":
        return render(request, 'Single_people4.html')
    elif request.method == "POST":
        v = request.POST.getlist('Company_nature')
        EAD = float(v[0])
        Company_nature_value = list(Company_nature.objects.filter(Type=v[1]).values_list('Coefficient', flat=True))
        Issuer_industry_value= list(Issuer_industry.objects.filter(Type=v[2]).values_list('Coefficient', flat=True))
        Credit_environment_value= list(Credit_environment.objects.filter(Type=v[3]).values_list('Coefficient', flat=True))
        Bond_type_value= list(Bond_type.objects.filter(Type=v[4]).values_list('Coefficient', flat=True))
        Guarantee_money = float(v[5])
        Guarantor_type_value= list(Guarantor_type.objects.filter(Type=v[6]).values_list('Coefficient', flat=True))
        Guarantee_type_value = list(Guarantee_type.objects.filter(Type=v[7]).values_list('Coefficient', flat=True))
        Guarantee_strength_value = list(Guarantee_strength.objects.filter(Type=v[8]).values_list('Coefficient', flat=True))
        Collateral_money = float(v[9])
        Collateral_depend_value = list(Collateral_depend.objects.filter(Type=v[10]).values_list('Coefficient', flat=True))
        Collateral_type_value = list(Collateral_type.objects.filter(Type=v[11]).values_list('Coefficient', flat=True))
        Collateral_control_value = list(Collateral_control.objects.filter(Type=v[12]).values_list('Coefficient', flat=True))
        Collateral_environment_value = list(Collateral_environment.objects.filter(Type=v[13]).values_list('Coefficient', flat=True))

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
        Collateral_coefficient = Collateral_money * Collateral_type_value[0] * Collateral_control_value[0] * \
                                 Collateral_depend_value[0] * Collateral_environment_value[0]
        print  '抵质押品有效缓释值:', Collateral_coefficient

        # 担保人有效缓释值
        # print Guarantee_money,Guarantor_type_value[0],Guarantee_strength_value[0],Guarantee_type_value[0]
        Guarantor__coefficient = Guarantee_money * Guarantor_type_value[0] * Guarantee_strength_value[0] * Guarantee_type_value[0]
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
        print 'LGD值：', LGD_value

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

        '''
        返回json字符串
        '''
        list_value = [Debtor_coefficient, Bond_coefficient, Collateral_coefficient, Guarantor__coefficient,
                      OriginalRecycling_value
            , BasisRecycling_value, LGD_value, LGD_level]
        dict_value = {}
        dict_value['json_str'] = list_value
        json_str = json.dumps(dict_value)
        print type(json_str)
        return HttpResponse(json_str)

    else:
        # PUT,DELETE,HEAD,OPTION...
        return redirect('/Single_people4/')

#场景五：单发行人多抵押无担保（暂支持两个抵押）
def Single_people5(request):
    if request.method == "GET":
        return render(request, 'Single_people5.html')
    elif request.method == "POST":
        v = request.POST.getlist('Company_nature')
        EAD = float(v[0])
        Company_nature_value = list(Company_nature.objects.filter(Type=v[1]).values_list('Coefficient', flat=True))
        Issuer_industry_value = list(Issuer_industry.objects.filter(Type=v[2]).values_list('Coefficient', flat=True))
        Credit_environment_value = list(Credit_environment.objects.filter(Type=v[3]).values_list('Coefficient', flat=True))
        Bond_type_value = list(Bond_type.objects.filter(Type=v[4]).values_list('Coefficient', flat=True))
        Collateral_money1 = float(v[5])
        Collateral_depend_value1 = list(Collateral_depend.objects.filter(Type=v[6]).values_list('Coefficient', flat=True))
        Collateral_type_value1 = list(Collateral_type.objects.filter(Type=v[7]).values_list('Coefficient', flat=True))
        Collateral_control_value1 = list(Collateral_control.objects.filter(Type=v[8]).values_list('Coefficient', flat=True))
        Collateral_environment_value1 = list(Collateral_environment.objects.filter(Type=v[9]).values_list('Coefficient', flat=True))
        Collateral_money2 = float(v[10])
        Collateral_depend_value2 = list(Collateral_depend.objects.filter(Type=v[11]).values_list('Coefficient', flat=True))
        Collateral_type_value2 = list(Collateral_type.objects.filter(Type=v[12]).values_list('Coefficient', flat=True))
        Collateral_control_value2 = list(Collateral_control.objects.filter(Type=v[13]).values_list('Coefficient', flat=True))
        Collateral_environment_value2 = list(Collateral_environment.objects.filter(Type=v[14]).values_list('Coefficient', flat=True))
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
        Collateral_coefficient = (Collateral_money1 * Collateral_type_value1[0] * Collateral_control_value1[0] * Collateral_depend_value1[0] * Collateral_environment_value1[0]+Collateral_money2 * Collateral_type_value2[0] * Collateral_control_value2[0] * Collateral_depend_value2[0] * Collateral_environment_value2[0])
        print  '抵质押品有效缓释值:', Collateral_coefficient

        # 担保人有效缓释值
        # print Guarantee_money,Guarantor_type_value[0],Guarantee_strength_value[0],Guarantee_type_value[0]
        Guarantor__coefficient =0
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
        print 'LGD值：', LGD_value
        list_value = [Debtor_coefficient, Bond_coefficient, Collateral_coefficient, Guarantor__coefficient,
                      OriginalRecycling_value
            , BasisRecycling_value, LGD_value]
        dict_value = {}
        dict_value['json_str'] = list_value
        json_str = json.dumps(dict_value)
        print type(json_str)
        return HttpResponse(json_str)

    else:
        # PUT,DELETE,HEAD,OPTION...
        return redirect('/Single_people5/')

#场景六：单发行人无抵押多担保（暂支持两个担保）
def Single_people6(request):
    if request.method == "GET":
        return render(request, 'Single_people6.html')
    elif request.method == "POST":
        v = request.POST.getlist('Company_nature')
        EAD = float(v[0])
        Company_nature_value = list(Company_nature.objects.filter(Type=v[1]).values_list('Coefficient', flat=True))
        Issuer_industry_value= list(Issuer_industry.objects.filter(Type=v[2]).values_list('Coefficient', flat=True))
        Credit_environment_value= list(Credit_environment.objects.filter(Type=v[3]).values_list('Coefficient', flat=True))
        Bond_type_value= list(Bond_type.objects.filter(Type=v[4]).values_list('Coefficient', flat=True))
        Guarantee_money1 = float(v[5])
        Guarantor_type_value1 = list(Guarantor_type.objects.filter(Type=v[6]).values_list('Coefficient', flat=True))
        Guarantee_type_value1 = list(Guarantee_type.objects.filter(Type=v[7]).values_list('Coefficient', flat=True))
        Guarantee_strength_value1 = list(Guarantee_strength.objects.filter(Type=v[8]).values_list('Coefficient', flat=True))
        Guarantee_money2 = float(v[9])
        Guarantor_type_value2 = list(Guarantor_type.objects.filter(Type=v[10]).values_list('Coefficient', flat=True))
        Guarantee_type_value2 = list(Guarantee_type.objects.filter(Type=v[11]).values_list('Coefficient', flat=True))
        Guarantee_strength_value2 = list(Guarantee_strength.objects.filter(Type=v[12]).values_list('Coefficient', flat=True))
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
        Guarantor__coefficient = (Guarantee_money1 * Guarantor_type_value1[0] * Guarantee_strength_value1[0] * \
                                 Guarantee_type_value1[0]+Guarantee_money2 * Guarantor_type_value2[0] * Guarantee_strength_value2[0] * \
                                 Guarantee_type_value2[0])
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
        print 'LGD值：', LGD_value
        list_value = [Debtor_coefficient, Bond_coefficient, Collateral_coefficient, Guarantor__coefficient,
                      OriginalRecycling_value
            , BasisRecycling_value, LGD_value]
        dict_value = {}
        dict_value['json_str'] = list_value
        json_str = json.dumps(dict_value)
        print type(json_str)
        return HttpResponse(json_str)
    else:
        redirect('/Single_people6.html/')

#场景七：单发行人多抵押多担保（暂时支持两个抵押两个担保）
def Single_people7(request):
    if request.method == "GET":
        return render(request, 'Single_people7.html')
    elif request.method == "POST":
        v = request.POST.getlist('Company_nature')
        EAD = float(v[0])
        Company_nature_value = list(Company_nature.objects.filter(Type=v[1]).values_list('Coefficient', flat=True))
        Issuer_industry_value= list(Issuer_industry.objects.filter(Type=v[2]).values_list('Coefficient', flat=True))
        Credit_environment_value= list(Credit_environment.objects.filter(Type=v[3]).values_list('Coefficient', flat=True))
        Bond_type_value= list(Bond_type.objects.filter(Type=v[4]).values_list('Coefficient', flat=True))
        Collateral_money1 = float(v[5])
        Collateral_depend_value1 = list(Collateral_depend.objects.filter(Type=v[6]).values_list('Coefficient', flat=True))
        Collateral_type_value1 = list(Collateral_type.objects.filter(Type=v[7]).values_list('Coefficient', flat=True))
        Collateral_control_value1 = list(Collateral_control.objects.filter(Type=v[8]).values_list('Coefficient', flat=True))
        Collateral_environment_value1 = list( Collateral_environment.objects.filter(Type=v[9]).values_list('Coefficient', flat=True))
        Collateral_money2 = float(v[10])
        Collateral_depend_value2 = list(Collateral_depend.objects.filter(Type=v[11]).values_list('Coefficient', flat=True))
        Collateral_type_value2 = list(Collateral_type.objects.filter(Type=v[12]).values_list('Coefficient', flat=True))
        Collateral_control_value2 = list(Collateral_control.objects.filter(Type=v[13]).values_list('Coefficient', flat=True))
        Collateral_environment_value2 = list(Collateral_environment.objects.filter(Type=v[14]).values_list('Coefficient', flat=True))
        Guarantee_money1 = float(v[15])
        Guarantor_type_value1= list(Guarantor_type.objects.filter(Type=v[16]).values_list('Coefficient', flat=True))
        Guarantee_type_value1 = list(Guarantee_type.objects.filter(Type=v[17]).values_list('Coefficient', flat=True))
        Guarantee_strength_value1 = list(Guarantee_strength.objects.filter(Type=v[18]).values_list('Coefficient', flat=True))
        Guarantee_money2 = float(v[19])
        Guarantor_type_value2 = list(Guarantor_type.objects.filter(Type=v[20]).values_list('Coefficient', flat=True))
        Guarantee_type_value2 = list(Guarantee_type.objects.filter(Type=v[21]).values_list('Coefficient', flat=True))
        Guarantee_strength_value2 = list(Guarantee_strength.objects.filter(Type=v[22]).values_list('Coefficient', flat=True))

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
        Collateral_coefficient = (Collateral_money1 * Collateral_type_value1[0] * Collateral_control_value1[0] * Collateral_depend_value1[0] * Collateral_environment_value1[0]+Collateral_money2 * Collateral_type_value2[0] * Collateral_control_value2[0] * Collateral_depend_value2[0] * Collateral_environment_value2[0])
        print  '抵质押品有效缓释值:', Collateral_coefficient

        # 担保人有效缓释值
        # print Guarantee_money,Guarantor_type_value[0],Guarantee_strength_value[0],Guarantee_type_value[0]
        Guarantor__coefficient = (Guarantee_money1 * Guarantor_type_value1[0] * Guarantee_strength_value1[0] * \
                                 Guarantee_type_value1[0]+Guarantee_money2 * Guarantor_type_value2[0] * Guarantee_strength_value2[0] * \
                                 Guarantee_type_value2[0])
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
        print 'LGD值：', LGD_value
        list_value = [Debtor_coefficient, Bond_coefficient, Collateral_coefficient, Guarantor__coefficient,
                      OriginalRecycling_value
            , BasisRecycling_value, LGD_value]
        dict_value = {}
        dict_value['json_str'] = list_value
        json_str = json.dumps(dict_value)
        print type(json_str)
        return HttpResponse(json_str)

    else:
        # PUT,DELETE,HEAD,OPTION...
        return redirect('/Single_people7/')

#场景八：多发行无抵押无担保（暂时支持两个发行人）
def Single_people8(request):
    if request.method == "GET":
        return render(request, 'Single_people8.html')
    elif request.method == "POST":
        v = request.POST.getlist('Company_nature')
       # issuer_one =
        EAD = float(v[2])
        Company_nature_value = list(Company_nature.objects.filter(Type=v[3]).values_list('Coefficient', flat=True))
        Issuer_industry_value = list(Issuer_industry.objects.filter(Type=v[4]).values_list('Coefficient', flat=True))
        Credit_environment_value = list(Credit_environment.objects.filter(Type=v[5]).values_list('Coefficient', flat=True))
        Bond_type_value = list(Bond_type.objects.filter(Type=v[6]).values_list('Coefficient', flat=True))
        # 计算方法
        # 债务人调整系数
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
        if (Collateral_coefficient + Guarantor__coefficient) > 1.05:
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

        #LGD级别

        if LGD_value >= -99999 and LGD_value < 0.1:
            LGD_level = 'LGD1'
        elif LGD_value >= 0.1 and LGD_value < 0.2:
            LGD_level = 'LGD2'
        elif LGD_value >= 0.2 and LGD_value < 0.3:
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


        #发行人有效认定评级平均违约率
        a = str(v[0]).replace('u\'', '\'')
        b = a.decode('unicode_escape')
        a_int = float(b)
        c = str(v[1]).replace('u\'', '\'')
        d = c.decode('unicode_escape')
        c_int = float(d)
        Company_avg = (a_int + c_int) / 2
        print Company_avg

        '''
        通过发行人(两个)平均违约率映射主表尺表
        '''

        if Company_avg >= 0 and Company_avg < 0.00002:
            Body_basisRatting = 'A1'
        elif Company_avg >= 0.00002 and Company_avg < 0.00006:
            Body_basisRatting = 'A2'
        elif Company_avg >= 0.00006 and Company_avg < 0.00013:
            Body_basisRatting = 'A3'
        elif Company_avg >= 0.00013 and Company_avg < 0.00023:
            Body_basisRatting = 'B1'
        elif Company_avg >= 0.00023 and Company_avg < 0.00040:
            Body_basisRatting = 'B2'
        elif Company_avg >= 0.00040 and Company_avg < 0.00070:
            Body_basisRatting = 'B3'
        elif Company_avg >= 0.00070 and Company_avg < 0.00122:
            Body_basisRatting = 'C1'
        elif Company_avg >= 0.00122 and Company_avg < 0.00213:
            Body_basisRatting = 'C2'
        elif Company_avg >=0.00213 and Company_avg < 0.00372:
            Body_basisRatting = 'C3'
        elif Company_avg >= 0.00372 and Company_avg <= 0.00648:
            Body_basisRatting = 'D1'
        elif Company_avg >= 0.00648 and Company_avg <= 0.01131:
            Body_basisRatting = 'D2'
        elif Company_avg >= 0.01131 and Company_avg <= 0.01972:
            Body_basisRatting = 'D3'
        elif Company_avg >= 0.01972 and Company_avg <= 0.03441:
            Body_basisRatting = 'E1'
        elif Company_avg >= 0.03441 and Company_avg <= 0.06002:
            Body_basisRatting = 'E2'
        elif Company_avg >= 0.06002 and Company_avg <= 0.10469:
            Body_basisRatting = 'E3'
        elif Company_avg >= 0.10469 and Company_avg <= 0.18262:
            Body_basisRatting = 'F1'
        elif Company_avg >= 0.18262 and Company_avg <= 0.31856:
            Body_basisRatting = 'F2'
        elif Company_avg >=  0.31856 and Company_avg <= 1:
            Body_basisRatting = 'F3'
        else:
            Body_basisRatting = '评级太高，找不到！'
        print 'LGD级别：', Body_basisRatting
        '''
        通过主体评级、LGD级别得出债券基础评级
        '''
        if LGD_level== 'LGD1' and Body_basisRatting[0] ==1 :
            Bond_basisRatting = Body_basisRatting
        elif LGD_level== 'LGD1' and Body_basisRatting[0]==2:
            Bond_basisRatting = list(Ratting_master_scale.objects.filter(ID=1).values_list('Ratting', flat=True))
        elif LGD_level== 'LGD2' and Body_basisRatting[0]==1:
            Bond_basisRatting = Body_basisRatting
        elif LGD_level == 'LGD1' and Body_basisRatting[0] < 2:
            Bond_basisRatting = list(Ratting_master_scale.objects.filter(ID=(Body_basisRatting[0])-2).values_list('Ratting', flat=True))
        elif LGD_level == LGD_level== 'LGD2' and Body_basisRatting[0] <2:
            Bond_basisRatting = list(Ratting_master_scale.objects.filter(ID=(Body_basisRatting[0]) - 1).values_list('Ratting', flat=True))
        else:
            Bond_basisRatting = Body_basisRatting
        print Bond_basisRatting
        list_value = [Debtor_coefficient, Bond_coefficient, Collateral_coefficient, Guarantor__coefficient, OriginalRecycling_value
        , BasisRecycling_value, LGD_value,LGD_level,Body_basisRatting,Bond_basisRatting]
        dict_value = {}
        dict_value['json_str'] = list_value
        json_str = json.dumps(dict_value)
        return HttpResponse(json_str)
    else:
        # PUT,DELETE,HEAD,OPTION...
        return redirect('/Single_people8/')

def login(request):
    if request.method == "GET":
        return render(request, 'hello.html')
    elif request.method == "POST":
        v = request.POST.getlist('Company_nature')
        EAD = float(v[0])
        Company_nature_value = list(Company_nature.objects.filter(Type=v[1]).values_list('Coefficient', flat=True))
        Issuer_industry_value= list(Issuer_industry.objects.filter(Type=v[2]).values_list('Coefficient', flat=True))
        Credit_environment_value= list(Credit_environment.objects.filter(Type=v[3]).values_list('Coefficient', flat=True))
        Bond_type_value= list(Bond_type.objects.filter(Type=v[4]).values_list('Coefficient', flat=True))
        Guarantee_money = float(v[5])
        Guarantor_type_value= list(Guarantor_type.objects.filter(Type=v[6]).values_list('Coefficient', flat=True))
        Guarantee_type_value = list(Guarantee_type.objects.filter(Type=v[7]).values_list('Coefficient', flat=True))
        Guarantee_strength_value = list(Guarantee_strength.objects.filter(Type=v[8]).values_list('Coefficient', flat=True))
        Collateral_money = float(v[9])
        Collateral_depend_value = list(Collateral_depend.objects.filter(Type=v[10]).values_list('Coefficient', flat=True))
        Collateral_type_value = list(Collateral_type.objects.filter(Type=v[11]).values_list('Coefficient', flat=True))
        Collateral_control_value = list(Collateral_control.objects.filter(Type=v[12]).values_list('Coefficient', flat=True))
        Collateral_environment_value = list(Collateral_environment.objects.filter(Type=v[13]).values_list('Coefficient', flat=True))

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
        Collateral_coefficient = Collateral_money * Collateral_type_value[0] * Collateral_control_value[0] * \
                                 Collateral_depend_value[0] * Collateral_environment_value[0]
        print  '抵质押品有效缓释值:', Collateral_coefficient

        # 担保人有效缓释值
        # print Guarantee_money,Guarantor_type_value[0],Guarantee_strength_value[0],Guarantee_type_value[0]
        Guarantor__coefficient = Guarantee_money * Guarantor_type_value[0] * Guarantee_strength_value[0] * Guarantee_type_value[0]
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
        print 'LGD值：', LGD_value
        # print Issuer_industry_value[0]
        # print Bond_type_value[0]

        # a = str(v).replace('u\'', '\'')
        # s = a.decode('unicode_escape')
        # print s
        # print v[0]

        return render(request, 'hello.html')

    else:
        # PUT,DELETE,HEAD,OPTION...
        return redirect('/hello/')
def test(request):
    data = { "factorCode": "BOND_TYPE",
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
    result = [(item.get('name')) for item in data['options']]
    return render(request, 'test.html', {"obj": result})


# if __name__ == '__main__':
#     test()




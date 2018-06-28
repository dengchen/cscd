# -*- coding: utf-8 -*-
from django import forms
'''
1.无抵押无担保  noPledgeGuarantee
2.无抵押单担保  noPledgeOneGuarantee
3.单抵押无担保  onePledgeNoGuarantee
4.单抵押单担保  onePledgeOneGuarantee

'''

class noPledgeGuarantee(forms.Form):
    bondBalance = forms.CharField()
    bondType = forms.CharField()
    companyNature = forms.CharField()
    creditRegion = forms.CharField()
    industary = forms.CharField()
    companyRating =forms.CharField()


class  noPledgeOneGuarantee(forms.Form):
        bondBalance = forms.CharField()
        bondType = forms.CharField()
        companyNature = forms.CharField()
        creditRegion = forms.CharField()
        industary = forms.CharField()
        warrantyMoney = forms.CharField()
        guaranteeType = forms.CharField()
        warrantyStrength = forms.CharField()
        warrantorType = forms.CharField()
        warrantorRating = forms.CharField()
        companyRating = forms.CharField()

class onePledgeNoGuarantee(forms.Form):
    bondBalance = forms.CharField()
    bondType = forms.CharField()
    companyNature = forms.CharField()
    creditRegion = forms.CharField()
    industary = forms.CharField()
    pledgeMoney = forms.CharField()
    pledgeDepend = forms.CharField()
    pledgeControl = forms.CharField()
    pledgeType = forms.CharField()
    pledgeRegion = forms.CharField()
    companyRating = forms.CharField()


class onePledgeOneGuarantee(forms.Form):
    bondBalance = forms.CharField()
    bondType = forms.CharField()
    companyNature = forms.CharField()
    creditRegion = forms.CharField()
    industary = forms.CharField()
    pledgeMoney = forms.CharField()
    pledgeDepend = forms.CharField()
    pledgeControl = forms.CharField()
    pledgeType = forms.CharField()
    pledgeRegion = forms.CharField()
    warrantyMoney = forms.CharField()
    guaranteeType = forms.CharField()
    warrantyStrength = forms.CharField()
    warrantorType = forms.CharField()
    warrantorRating = forms.CharField()
    companyRating = forms.CharField()



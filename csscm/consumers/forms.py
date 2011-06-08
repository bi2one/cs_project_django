# -*- coding: utf-8 -*-

import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from csscm.consumers.models import SellingItem

class JoinForm(forms.Form) :
    username = forms.CharField(max_length=30, label="사용자id", required=True)
    password = forms.CharField(max_length=128, label="비밀번호", widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=128, label="비밀번호(확인용)", widget=forms.PasswordInput())
    nick_name = forms.CharField(max_length=30, label="닉네임", required=True)
    email = forms.EmailField(label="이메일")
    member_type = forms.ChoiceField(label="멤버타입", choices=[("consumer", "consumer"),
                                                               ("retailer", "retailer"),
                                                               ("wholesaler", "wholesaler"),
                                                               ("factory", "factory"),
                                                               ("manager", "manager")])

    def clean_password_confirm(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_confirm = self.cleaned_data['password_confirm']
        if password == '':
            forms.ValidationError('필수항목 입니다.')
        if password == password_confirm:
            return password_confirm
        raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^[a-zA-Z][a-zA-Z0-9]*$', username):
            raise forms.ValidationError('사용자 아이디는 알파벳으로 시작하고, 기호가 들어갈 수 없습니다.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('이미 사용중인 아이디 입니다.')

class OrderForm(forms.Form) :
    count = forms.CharField(label="주문수량", required=True)
    item_id = forms.CharField(label="제품아이디", widget=forms.HiddenInput())

class RegistStockItemForm(forms.Form) :
    name = forms.CharField(max_length=128, required=True)
    price = forms.CharField(max_length=128, required=True)
    description = forms.CharField(widget=forms.Textarea)
    count = forms.CharField(max_length=128, required=True)
    parent_member_id = forms.CharField(max_length=128, required=True)

    def clean_count(self):
        count = self.cleaned_data['item_count']

        try:
            if int(count) < 0:
                raise forms.ValidationError('0 이상의 값을 기입하셔야 합니다.')
            return count
        except ValueError:
            raise forms.ValidationError("숫자를 입력하셔야 합니다.")

    def clean_parent_member_id(self):
        member_id = self.cleaned_data['parent_member_id']

        try:
            if int(member_id) < 0:
                raise forms.ValidationError('0 이상의 값을 기입하셔야 합니다.')
            return member_id
        except ValueError:
            raise forms.ValidationError("숫자를 입력하셔야 합니다.")


    def clean_price(self):
        price = self.cleaned_data['price']

        try:
            if int(price) < 0:
                raise forms.ValidationError('0 이상의 값을 기입하셔야 합니다.')
            return price
        except ValueError:
            raise forms.ValidationError("숫자를 입력하셔야 합니다.")
    

class RegistItemForm(forms.Form) :
    desc_head = forms.CharField(widget=forms.Textarea)
    selling_count = forms.CharField(max_length=45, required=True)
    name = forms.CharField(max_length=128, required=True)
    price = forms.CharField(max_length=128, required=True)
    description = forms.CharField(widget=forms.Textarea)
    item_count = forms.CharField(max_length=128, required=True)
    parent_member_id = forms.CharField(max_length=128, required=True)

    def clean_selling_count(self):
        count = self.cleaned_data['selling_count']

        try:
            if int(count) < 0:
                raise forms.ValidationError('0 이상의 값을 기입하셔야 합니다.')
            return count
        except ValueError:
            raise forms.ValidationError("숫자를 입력하셔야 합니다.")
    
    def clean_item_count(self):
        count = self.cleaned_data['item_count']

        try:
            if int(count) < 0:
                raise forms.ValidationError('0 이상의 값을 기입하셔야 합니다.')
            return count
        except ValueError:
            raise forms.ValidationError("숫자를 입력하셔야 합니다.")

    def clean_price(self):
        price = self.cleaned_data['price']

        try:
            if int(price) < 0:
                raise forms.ValidationError('0 이상의 값을 기입하셔야 합니다.')
            return price
        except ValueError:
            raise forms.ValidationError("숫자를 입력하셔야 합니다.")
        
    def clean_parent_member_id(self):
        member_id = self.cleaned_data['parent_member_id']

        try:
            if int(member_id) < 0:
                raise forms.ValidationError('0 이상의 값을 기입하셔야 합니다.')
            return member_id
        except ValueError:
            raise forms.ValidationError("숫자를 입력하셔야 합니다.")

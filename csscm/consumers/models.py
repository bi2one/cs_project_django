# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Member(models.Model):
    user = models.ForeignKey(User)
    member_type = models.CharField(max_length=128)

class Item(models.Model):
    member = models.ForeignKey(Member, related_name="stock_member")
    parent_item = models.ForeignKey('self', null=True)
    
    name = models.CharField(max_length=128)
    price = models.PositiveIntegerField()
    description = models.TextField()
    count = models.PositiveIntegerField()
    image = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class SellingItem(models.Model):
    item = models.ForeignKey(Item)
    member = models.ForeignKey(Member)
    
    desc_head = models.TextField()
    count = models.PositiveIntegerField()
    state = models.CharField(max_length=128)

    created = models.DateTimeField(auto_now_add=True)

class BuyingItem(models.Model):
    from_member = models.ForeignKey(Member, related_name="from_member")
    to_member = models.ForeignKey(Member, related_name="to_member")
    item = models.ForeignKey(Item)
    
    count = models.PositiveIntegerField()
    account = models.CharField(max_length=128)
    item_state = models.CharField(max_length=128)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Report(models.Model):
    member = models.ForeignKey(Member)
    
    filename = models.CharField(max_length=128)
    
    created = models.DateTimeField(auto_now_add=True)

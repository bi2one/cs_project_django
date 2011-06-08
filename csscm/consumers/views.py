# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from csscm.consumers.models import SellingItem, Member, BuyingItem, Item
from csscm.consumers.forms import JoinForm, OrderForm, RegistItemForm

def index(request):
    form = AuthenticationForm(request)
    user = request.user
    loginError = login_user(request)
    member = None
    consumer_items = None
    
    items = SellingItem.objects.all()

    if not user.is_anonymous():
        members = Member.objects.filter(user=user)
        if (len(members) != 0):
            member = Member.objects.filter(user=user)[0]
            consumer_items = BuyingItem.objects.filter(from_member=member)
    
    variables = RequestContext(request, {
        'form' : form,
        'items': items,
        'member': member,
        'loginError' : loginError,
        'consumer_items' : consumer_items,
        })

    
    return render_to_response('index.html',
                              variables,
                              context_instance=RequestContext(request))
    
    
def login_user(request):
    isError = False
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            isError = True

    return isError;

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect('/')
    return response

def join_user(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)

        if form.is_valid():
            # save user
            username = form.cleaned_data['username']
            nick_name = form.cleaned_data['nick_name']
            password = form.cleaned_data['password']
            member_type = form.cleaned_data['member_type']
            user = User(
                username = username,
                nick_name = nick_name,
                password = '',
                email = form.cleaned_data['email']
            )
            user.set_password(password)
            user.save()

            member = Member(
                user = user,
                member_type = member_type
                )
            member.save();
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
            # return login_user(request)
    else:
        form = JoinForm()

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'join.html',
        variables
    )

def refund_buyingitem(request, item_id):
    refund_items = BuyingItem.objects.filter(id=item_id)

    if (len(refund_items) != 0):
        refund_item = refund_items[0]
        refund_item.item_state = "refund"
        refund_item.save()
        
    return HttpResponseRedirect('/')

def itemview(request, item_id) :
    view_items = SellingItem.objects.filter(id=item_id)
    view_item = None
    member = None
    user = request.user

    if not user.is_anonymous():
        members = Member.objects.filter(user=user)
        if (len(members) != 0):
            member = members[0]

    if (len(view_items) == 0):
        return HttpResponseRedirect('/')
    else:
        view_item = view_items[0]

    form = OrderForm({
        'item_id' : item_id
        })
        
    variables = RequestContext(request, {
        'item': view_item,
        'form': form,
        'member': member,
        })

    return render_to_response('itemview.html',
                              variables,
                              context_instance=RequestContext(request)
                              )

def order(request):
    member = None
    user = request.user
    item = None

    if request.method == 'POST':
        form = OrderForm(request.POST)
        item_id = request.POST['item_id']

        items = SellingItem.objects.filter(id=item_id)
        user = request.user

        if not user.is_anonymous():
            members = Member.objects.filter(user=user)
            if (len(members) != 0):
                member = members[0]
            else :
                return HttpResponseRedirect('/')
        else :
            return HttpResponseRedirect('/')

        if (len(items) == 0):
            return HttpResponseRedirect('/')
        else:
            item = items[0]


        if form.is_valid():
            error = None
            count = form.cleaned_data['count']

            if int(count) > int(item.count):
                error = '요청 수량이 제품 보유량보다 큽니다.'
            if int(count) <= 0:
                error = '제품 요청은 0보다 큰 수량으로 하셔야 합니다'

            if error is not None:
                variables = RequestContext(request, {
                    'form': form,
                    'error': error,
                    'item': item,
                    'member': member,
                })
                return render_to_response('itemview.html',
                                          variables,
                                          context_instance=RequestContext(request)
                                          )
            

            # 정상일때 저장
            item.count = str(int(item.count) - int(count))
            item.save()

            buying_item = BuyingItem(count = int(count),
                                     account = getVirtualAccount(),
                                     item_state = "accept",
                                     from_member = member,
                                     to_member = item.member,
                                     item = item.item)
            buying_item.save()
                                     
            return HttpResponseRedirect('/')

        variables = RequestContext(request, {
            'form': form,
            'item': item,
            'member': member,
            })
        return render_to_response('itemview.html',
                                  variables,
                                  context_instance=RequestContext(request)
                                  )
    else:
        return HttpResponseRedirect('/')

def getVirtualAccount():
    return "virtual account number"

def getMemberByUser(user):
    member = None

    if not user.is_anonymous():
        members = Member.objects.filter(user=user)
        if (len(members) != 0):
            member = Member.objects.filter(user=user)[0]

    return member

def manage(request):
    member = getMemberByUser(request.user)

    if member is None:
        return HttpResponseRedirect('/')

    if member.member_type == "retailer":
        return retailer_manager(request)
    elif member.member_type == "wholesaler":
        return wholesaler_manager(request)
    elif member.member_type == "factory":
        return factory_manager(request)
    elif member.member_type == "" or member.member_type == "manager":
        return account_manager(request)
    else:
        return HttpResponseRedirect('/')
    
def retailer_manager(request):
    member = getMemberByUser(request.user)

    if member is None:
        return HttpResponseRedirect('/')
    
    buying_items = BuyingItem.objects.filter(to_member = member)
    selling_items = SellingItem.objects.filter(member = member)
    stock_items = Item.objects.filter(member = member)

    variables = RequestContext(request, {
        'buying_items': buying_items,
        'selling_items': selling_items,
        'stock_items': stock_items,
        })

    return render_to_response("retailer_manager.html",
                              variables,
                              context_instance=RequestContext(request))

def wholesaler_manager(request):
    return HttpResponseRedirect('/')

def factory_manager(request):
    return HttpResponseRedirect('/')

def account_manager(request):
    return HttpResponseRedirect('/')

def finish_order(request, buying_item_id):
    member = getMemberByUser(request.user)

    if member is None:
        return HttpResponseRedirect('/')

    buying_items = BuyingItem.objects.filter(id=buying_item_id)

    if len(buying_items) == 0:
        return HttpResponseRedirect('/')

    buying_item = buying_items[0]

    if buying_item.to_member.id != member.id:
        return HttpResponseRedirect('/')
    else:
        buying_item.item_state = "finish"
        buying_item.save()

        buying_item.item.count = int(buying_item.item.count) - int(buying_item.count)
        
        if (buying_item.item.count < 0):
            buying_item.item.count = 0

        if (buying_item.item.count < 5) :
            if len(BuyingItem.objects.filter(item=buying_item.item).filter(item_state="accept")) == 0:
                retailer_buying_item = BuyingItem(from_member = member,
                                                  to_member = buying_item.item.parent_member,
                                                  count = 5,
                                                  item_state = "accept",
                                                  account = getVirtualAccount(),
                                                  item = buying_item.item)
                retailer_buying_item.save()
        
        buying_item.item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def refund_order(request, buying_item_id):
    member = getMemberByUser(request.user)

    if member is None:
        return HttpResponseRedirect('/')

    buying_items = BuyingItem.objects.filter(id=buying_item_id)

    if len(buying_items) == 0:
        return HttpResponseRedirect('/')

    buying_item = buying_items[0]

    if buying_item.to_member.id != member.id:
        return HttpResponseRedirect('/')
    else:
        buying_item.item_state = "finish_refund"
        buying_item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def update_selling_item(request, selling_item_id = None) :
    member = getMemberByUser(request.user)
    wholesalers = Member.objects.filter(member_type = "wholesaler")

    if member is None or member.member_type == "consumer":
        return HttpResponseRedirect('/')
    
    if request.method == 'POST':
        form = RegistItemForm(request.POST)

        if form.is_valid():
            desc_head = form.cleaned_data['desc_head']
            selling_count = form.cleaned_data['selling_count']
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            item_count = form.cleaned_data['item_count']
            parent_member_id = form.cleaned_data['parent_member_id']

            item = Item(
                name = name,
                price = price,
                description = description,
                count = item_count,
                parent_member = Member.objects.get(id=parent_member_id),
                member = member
                )
            selling_item = SellingItem(
                desc_head = desc_head,
                count = selling_count,
                price = price,
                member = member
                )

            if selling_item_id is not None:
                selling_items = SellingItem.objects.filter(id=selling_item_id)
                filtered_selling_item = None
                if (len(selling_items) == 0):
                    return HttpResponseRedirect('/')
                else:
                    filtered_selling_item = selling_items[0]

                if filtered_selling_item.member.id != selling_item.member.id:
                    return HttpResponseRedirect('/')
                else :
                    item.id = filtered_selling_item.item.id
                    selling_item.id = filtered_selling_item.id

            now = datetime.datetime.now()
            item.created = now
            selling_item.created = now
            item.save()
            selling_item.item = item
            selling_item.save()
            
            return HttpResponseRedirect('/manage/')
        else:
            variables = RequestContext(request, {
                'form': form,
                'wholesalers': wholesalers,
                })
            return render_to_response('update_selling_item.html',
                                      variables,
                                      context_instance=RequestContext(request)
                                      )
    else :
        form = None
        if selling_item_id is not None:
            selling_items = SellingItem.objects.filter(id=selling_item_id)

            if len(selling_items) == 0:
                return HttpResponseRedirect('/')

            selling_item = selling_items[0]
            
            form = RegistItemForm({
                'desc_head': selling_item.desc_head,
                'selling_count': selling_item.count,
                'name': selling_item.item.name,
                'price': selling_item.item.price,
                'description': selling_item.item.description,
                'item_count': selling_item.item.count,
                'parent_member_id': selling_item.item.parent_member.id
                })
        else :
            form = RegistItemForm()

        variables = RequestContext(request, {
            'form': form,
            'wholesalers': wholesalers,
            })
        
        return render_to_response('update_selling_item.html',
                                  variables,
                                  context_instance=RequestContext(request)
                                  )


def update_item(request, item_id) :
    item = Item.objects.get(id=item_id)
    selling_items = SellingItem.objects.filter(item=item)
    if len(selling_items) == 0:
        return HttpResponseRedirect('/')

    return update_selling_item(request, selling_items[0].id)

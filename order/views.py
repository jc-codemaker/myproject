from django.shortcuts import render,redirect
from user import user_state
from shopping_cart.models import *
from order.models import *
from django.core.paginator import Paginator
from django.db import transaction
from datetime import *
# Create your views here.

@user_state.login
def order(request):
    user = User.objects.get(uname = request.session['currentUser'])
    cart_ids = request.GET.getlist('cart_ids')
    cart_ids2 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in = cart_ids2)
    cart_ids = ','.join(cart_ids)

    phone = user.uphone
    uphone = phone[:3] + '****' + phone[7:]
    context = {
        'title':'提交订单',
        'carts':carts,
        'user':user,
        'cart_ids':cart_ids,
        'uphone': uphone,
    }
    return render(request,'order/order.html',context)


@user_state.login
@transaction.atomic
def order_handle(request):
    tran_id = transaction.savepoint()
    cart_ids = request.POST.get('cart_ids')

    try:
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['currentUser']
        order.oid = '%s%s'%(uid,now.strftime('%Y%m%d%H%M%S'))
        order.userinfo_id = uid
        order.odate = now
        order.oaddress = request.POST.get('address')
        order.ototal = 0
        order.save()

        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        total = 0
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.orderinfo = order
            cart = CartInfo.objects.get(id = id1)
            goods = cart.goodsinfo
            if goods.gstock >= cart.count:
                goods.gstock = goods.gstock-cart.count
                goods.save()

                detail.goodsinfo = goods
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()

                total = total + goods.gprice*cart.count
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/shopping_cart/')

        order.ototal = total+10
        order.save()
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        transaction.savepoint_rollback(tran_id)

    return redirect('/order/order_list')







@user_state.login
def order_list(request,pindex):
    uname = request.session['currentUser']
    order_list = OrderInfo.objects.filter(userinfo_id = uname).order_by('-oid')
    paginator = Paginator(order_list,2)
    if pindex == '':
        pindex = '1'
    page = paginator.page(int(pindex))

    context = {
        'title':'用户中心',
        'page_name':1,
        'paginator':paginator,
        'page':page,
    }
    return render(request,'user/user_order.html',context)

@user_state.login
def pay(request,oid):
    order = OrderInfo.objects.get(oid = oid)
    order.oispay = True
    order.save()
    context = {'order':order}
    return render(request,'order/pay.html',context)


from django.shortcuts import render,redirect
from user import user_state
from shopping_cart.models import *
from django.http import JsonResponse
from goods.views import cart_count

# Create your views here.


# 获取当前状态，登录后可进行操作
@user_state.login
def shopping_cart(request):

    uid = request.session['currentUser']
    carts = CartInfo.objects.filter(userinfo_id = uid)
    context = {
        'title':'购物车',
        'page_name':1,
        'carts':carts
    }
    return render(request,'shopping_cart/cart.html',context)


@user_state.login
def add(request,gid,count):

    uid = request.session['currentUser']
    gid = int(gid)
    count = int(count)

    #　获取数据库中同时符合用户id和商品id的对象记录
    carts = CartInfo.objects.filter(userinfo_id = uid,goodsinfo_id = gid)
    # 如果对象已经存在于购物车中，则获取购物车中的对象，对该对象数量进行增加操作
    if len(carts)>=1:
        cart = carts[0]
        cart.count = cart.count + count
    # 如果对象不存在，则增加记录到数据库中
    else:
        cart = CartInfo()
        cart.userinfo_id = uid
        cart.goodsinfo_id = gid
        cart.count = count
    # 对数据进行保存
    cart.save()

    if request.is_ajax():
        count = cart_count(request)
        return JsonResponse({'count':count})
    else:
        return redirect('/shopping_cart/')


@user_state.login
def edit(request,cart_id,count):
    count1 = 1
    try:
        cart = CartInfo.objects.get(pk = int(cart_id))
        count1 = cart.count
        cart.count = int(count)
        cart.save()
        data = {'flag':1}
    except Exception as e:
        data = {'flag':count1}
    return JsonResponse(data)


@user_state.login
def delete(request,cart_id):
    try:
        cart = CartInfo.objects.get(pk = int(cart_id))
        cart.delete()
        data = {'flag':1}
    except Exception as e:
        data = {'flag':0}
    return JsonResponse(data)


from django.shortcuts import render
from django.http import *
from goods.models import *
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q,Sum
from shopping_cart.models import *
from user import user_state


import  json

# Create your views here.

# 主页，获取数据库中的信息并展示
def index(request):
    typelist = TypeInfo.objects.all()


    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type02 = typelist[0]

    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type12 = typelist[1]


    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type22 = typelist[2]

    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type32 = typelist[3]

    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type42 = typelist[4]

    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    type52 = typelist[5]

    context = {
        'type0':type0,'type01':type01,'type02':type02,
        'type1': type1, 'type11': type11,'type12':type12,
        'type2': type2, 'type21': type21,'type22':type22,
        'type3': type3, 'type31': type31,'type32':type32,
        'type4': type4, 'type41': type41,'type42':type42,
        'type5': type5, 'type51': type51,'type52':type52,
        'cart_count':cart_count(request)

    }
    return render(request, 'goods/index.html',context)


# 清空session缓存，退出登陆，重定向至主界面
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/goods/index')



# 商品详情展示
def detail(request,id):
    # 获取点击的商品对象
    goods = GoodsInfo.objects.get(pk = int(id))


    # 点击商品后，为商品的点击量属性+1，并保存至数据库
    goods.gclick = goods.gclick + 1
    goods.save()

    # 获取最新添加的商品信息
    news = goods.gtypeinfo.goodsinfo_set.order_by('-id')[0:2]

    # 准备上下文，传递参数
    context = {
        'title':goods.gtypeinfo.ttitle,
        'g':goods,
        'news':news,
        'id':id,
        'cart_count': cart_count(request)
    }

    response = render(request,'goods/detail.html',context)

    # 从cookie获取浏览的商品id，获取不到则返回‘’字符
    goods_ids = request.COOKIES.get('goods_ids','')
    # 如果浏览记录存在
    if goods_ids != '':
        # 以','为分割界线分割
        goods_ids1 = goods_ids.split(',')
        # 如果最新浏览的商品在所得列表中，则删除列表中存在的商品
        if goods_ids1.count(id) >= 1:
            goods_ids1.remove(id)
        # 将id添加在列表最前端
        goods_ids1.insert(0,id)
        # 如果cookie中储存的id多余5,则删除列表中第六个
        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = str(id)
    # 写入cookie
    response.set_cookie('goods_ids',goods_ids)

    return response




def goods_page(request):
    # 获取当前页码
    pagenow = int(request.GET.get('pagenow'))
    # 每页显示几条
    pageSize = 15
    # 总数据
    resultset = GoodsInfo.objects.filter(gtypeinfo=1).order_by('pk')
    # 构造Paganitor对象
    paginator = Paginator(resultset, pageSize)
    page = paginator.page(pagenow)
    # 准备上下文的数据
    content = {
        'goods_list': serializers.serialize('json', page.object_list),
        'page_range': json.dumps(paginator.page_range),
        'pagenow': pagenow
    }
    return JsonResponse(content)




# def goodslist(request,id):
#     # 获取所有类型对象
#     typelist = TypeInfo.objects.all()
#     # 获取请求id的对象
#     glist = TypeInfo.objects.get(pk = int(id))
#     # 获取最新添加的两个商品
#     newgoods = typelist[int(id)-1].goodsinfo_set.order_by('-id')[0:2]
#     # 按照id（添加顺序）对商品进行逆序排序
#     goods_id = typelist[int(id)-1].goodsinfo_set.order_by('-id')
#     # 按照价格对商品排序
#     goods_gprice = typelist[int(id) - 1].goodsinfo_set.order_by('gprice')
#     # 按照点击量对商品排序
#     goods_gclick = typelist[int(id) - 1].goodsinfo_set.order_by('-gclick')
#     # 准备上下文
#     context = {
#         'id':id,
#         'l':glist,
#         'newgoods':newgoods,
#         'goods_id':goods_id,
#         'goods_gprice':goods_gprice,
#         'goods_gclick':goods_gclick,
#         'title': glist.ttitle,
#
#     }
#     return render(request, 'goods/list.html',context)

def goodslist(request,id,pindex,sort):
    # id 为当前类型编号
    # pindex 为当前页码
    # sort 为当前排序方式


    # 获取请求id的对象
    glist = TypeInfo.objects.get(pk=int(id))
    # 获取最新添加的两个商品
    newgoods = glist.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':
        # 按照id（添加顺序）对商品进行逆序排序
        goods_list = GoodsInfo.objects.filter(gtypeinfo_id =int(id)).order_by('-id')
    elif sort =='2':
        # 按照价格对商品排序
        goods_list = GoodsInfo.objects.filter(gtypeinfo_id =int(id)).order_by('gprice')
    elif sort =='3':
        # 按照点击量对商品排序
        goods_list = GoodsInfo.objects.filter(gtypeinfo_id =int(id)).order_by('-gclick')

    pageinator = Paginator(goods_list,15)
    page = pageinator.page(int(pindex))

    context = {
        'title': glist.ttitle,
        'page':page,
        'pageinator':pageinator,
        'l':glist,
        'sort':sort,
        'newgoods':newgoods,
        'cart_count': cart_count(request)
    }
    return render(request, 'goods/list.html', context)


def goods_search(request):
    # 去除前后空格
    keyword = request.GET.get('keyword','').strip()
    sort = request.GET.get('sort','1')
    pindex = request.GET.get('pindex','1')

    goods_list = GoodsInfo.objects.filter(
        # 根据标题和内容进行模糊查询
        Q(gtitle__icontains =  keyword) | Q(gcontect__icontains = keyword) | Q(gintroduction__icontains = keyword)
    )
    if sort == '1':
        goods_list = goods_list.order_by('-id')
    elif sort == '2':
        goods_list = goods_list.order_by('gprice')
    elif sort == '3':
        goods_list = goods_list.order_by('-gclick')


    newgoods = GoodsInfo.objects.all().order_by('-id')[0:2]

    pageinator = Paginator(goods_list, 15)
    page = pageinator.page(pindex)

    context = {
        'title': '搜索商品',
        'page': page,
        'pageinator': pageinator,
        'l': None,
        'sort': sort,
        'newgoods': newgoods,
        'keyword':keyword,
        'cart_count': cart_count(request),
    }
    return render(request, 'goods/goods_search.html', context)

@user_state.login
def luck(request):
    return render(request, 'goods/luck.html')



def cart_count(request):

    count = 0
    user = request.session.get('currentUser')

    if user:
        ret = CartInfo.objects.filter(userinfo_id = user).aggregate(num=Sum('count'))
        count = ret['num']
    return count

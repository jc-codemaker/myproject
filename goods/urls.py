from django.conf.urls import include, url
from goods.views import *

urlpatterns = [
    url(r'^index$',index,name='index'),
    url(r'^logout$',logout,name='logout'),
    url(r'^(\d+)/$',detail),
    url(r'^list/(\d+)/(\d+)/(\d+)$', goodslist),
    url(r'^goods_search/$',goods_search,name='goods_search'),
    url(r'^luck$', luck, name='luck'),

    # url(r'^list(\d+)/(\d+)$', goodslist),
    # url(r'^goods_page$', goods_page, name='goods_page'),

]

from django.conf.urls import include, url
from order.views import *

urlpatterns=[
    url(r'^$',order, name='order'),
    url(r'^order_handle$', order_handle, name='order_handle'),
    url(r'^order_list(\d*)$', order_list, name='order_list'),
    url(r'^pay(\d+)$', pay, name='pay'),
]
from django.conf.urls import  url
from shopping_cart.views import *

urlpatterns=[
    url(r'^$',shopping_cart, name='shopping_cart'),
    url(r'^add/(\d+)/(\d+)$', add, name='add'),
    url(r'^edit(\d+)_(\d+)$', edit),
    url(r'^delete(\d+)$', delete),
]
from django.conf.urls import include, url
from user.views import *

urlpatterns = [
    url(r'^register$',register,name='register'),
    url(r'^login$',login,name='login'),
    url(r'^success$',success,name='success'),
    url(r'^result$',result,name='result'),
    url(r'^verification$', verification, name='verification'),
    url(r'^check_username$', check_username, name='check_username'),
    url(r'^check_userpwd$', check_userpwd, name='check_userpwd'),
    url(r'^check_userverification', check_userverification, name='check_userverification'),
    url(r'^user_center$',user_center,name='user_center'),
    url(r'^user_order$', user_order, name='user_order'),
    url(r'^user_address$', user_address, name='user_address'),
    url(r'^logout$', logout, name='logout'),
]

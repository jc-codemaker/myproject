from django.http import *

def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('currentUser'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login')
            red.set_cookie('url',request.get_full_path())
            return red
    return login_fun
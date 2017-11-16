from django.shortcuts import render
from user.models import *
from goods.models import *
from hashlib import *
import re
from django.http import *
from django.template import loader,RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import  StringIO,BytesIO
import random
from user import user_state

# 注册

def register(request):
    return render(request, 'user/register.html')




#  注册结果
def result(request):

    #   验证码验证
    context = {}
    userverification = request.POST.get('userverification')
    if request.session['codes'].upper() == userverification.upper():
        user = User()
        user.uname = request.POST.get('username')
        user.upwd=request.POST.get('userpwd')
        user.uemail = request.POST.get('uemail')
        user.upwd = sha1(user.upwd.encode('utf-8')).hexdigest()
        user.save()

        return HttpResponseRedirect('/user/login')
    else:
        return HttpResponseRedirect('/user/register')

    


#   登录
def login(request):

    #   用户勾选记住用户名时，下次登录调用本地cookies中的用户名
    context = {}
    username = request.COOKIES.get('user_name')
    # 如果用户名在cookie中，返回用户名到登陆界面
    if username:
        context['username']=username
        return render(request, 'user/login.html', context)
    else:
        return render(request,'user/login.html')




#   登录成功
#@csrf_exempt
def success(request):
    context = {}
    username = request.POST.get('username')
    userverification = request.POST.get('userverification')
    if request.session['codes'].upper() == userverification.upper():
        # 使用session实现状态保持
        request.session['currentUser'] = username
        response = HttpResponseRedirect('/goods/index')
        # 获取用户是否选择记住用户名
        remembername = request.POST.get('remembername')
        # 如果选中，将用户名写入cookie中，并设定过期时间
        if remembername=='1':
            response.set_cookie('user_name',username,max_age=3600)
        return response
    else:
        #登陆失败 则重定向至登录界面
        return HttpResponseRedirect('/user/login')



# 验证码生成


def verification(request):
    width = 120
    height = 30
    image = Image.new('RGB',(width,height),(255,255,255))
    font = ImageFont.truetype('/usr/share/fonts/truetype/padauk/Padauk.ttf',26)
    draw = ImageDraw.Draw(image)
    #添加噪点
    for x in range(width):
        for y in range(height):
            draw.point((x,y),fill=rndColor1())
    #设置验证码格式
    codes = ''
    for t in range(4):
        code = rndChar()
        codes += code
        draw.text((30*t + 5,0),code,font=font,fill=rndColor2())
    #images = images.filter(ImageFilter.BLUR)

    request.session['codes'] = codes
    request.session.set_expiry(0)

    f= BytesIO()
    image.save(f,'jpeg')
    return HttpResponse(f.getvalue(),'images/jpeg')

str1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def rndChar():
    return str1[random.randrange(0,len(str1))]
def rndColor1():
    return (random.randint(180, 255), random.randint(180, 255), random.randint(180, 255))
def rndColor2():
    return (random.randint(10, 200), random.randint(10, 200), random.randint(10, 200))



#   验证用户名是否存在
def check_username(request):
    username = request.GET.get('username')
    # 0不存在   1存在
    ret = '0'
    if len(User.objects.filter(uname=username)):
        ret = '1'
    return HttpResponse(ret)

#   验证密码是否正确
def check_userpwd(request):
    # 获取输入的密码，并对输入的密码进行加密
    userpwd = sha1(request.GET.get('userpwd').encode('utf-8')).hexdigest()

    # 0不存在   1存在
    ret = '0'
    if len(User.objects.filter(upwd=userpwd)):
        ret = '1'
    return HttpResponse(ret)


#   验证验证码是否正确
def check_userverification(request):
    # 获取输入的验证码
    userverification = request.GET.get('userverification')
    # 0不正确   1正确
    ret = '1'
    # 如果输入的验证码和session中的验证码不同，返回‘0’
    if request.session['codes'].upper() != userverification.upper():
        ret = '0'
    return HttpResponse(ret)




# 用户个人信息界面
# 装饰器获取session状态，存在则进入个人信息界面，否则跳转至登陆
@user_state.login
def user_center(request):
    user = User.objects.get(uname = request.session['currentUser'])

    goods_list = []
    goods_ids = request.COOKIES.get('goods_ids','')
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id = int(goods_id)))

    context = {
        'user':user,
        'goods_list':goods_list
    }
    return render(request, 'user/user_center.html',context)




# 用户全部订单界面
# 装饰器获取session状态，存在则进入全部订单界面，否则跳转至登陆
@user_state.login
def user_order(request):
    user = User.objects.get(uname = request.session['currentUser'])
    context = {
        'user':user
    }
    return render(request, 'user/user_order.html',context)



# 用户收货地址界面
# 装饰器获取session状态，存在则进入收货地址界面，否则跳转至登陆
@user_state.login
def user_address(request):
    #通过session键获取对象
    #首次访问是以GET方式获取数据 提交是POST方式
    user = User.objects.get(uname = request.session['currentUser'])
    if request.method=='POST':
        post = request.POST
        #获取输入信息，更改并保存至数据库
        user.ureceive = post.get('recipients')
        user.uaddress = post.get('Address')
        user.uzipcode = post.get('postcode')
        user.uphone = post.get('tel')
        user.save()
    # 获取手机号码 对手机号码进行字符串分割,拼接操作
    phone = user.uphone
    uphone = phone[:3]+'****'+phone[7:]
    # 准备上下文，并将上下文发送到收货地址界面
    context = {
        'user':user,
        'uphone':uphone,
    }
    return render(request, 'user/user_address.html',context)




#  退出登陆
def logout(request):
    #清除session缓存
    request.session.flush()
    #跳转至登录界面
    return render(request,'user/login.html')
    # return HttpResponseRedirect('/user/login')
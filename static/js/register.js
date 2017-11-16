/**
 * Created by time on 17-10-7.
 */

var xmlhttp;


function myajax(url,func,method='GET',params=null){
    //获取XMLHttpRequest对象

    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest()
    } else {
        xmlhttp = new ActiveXObject()
    }
    //onreadystatechange 事件
    xmlhttp.onreadystatechange = func;
    //open
    xmlhttp.open(method, url, true);
    //send
    xmlhttp.send(params);
};

//验证码更换
url = '/user/verification'
    function changeImage(obj){
        obj.src =  url+'?num='+new Date()
    }

//表单验证
window.onload = function () {
    var username = document.getElementById('username')
    var Password = document.getElementById('Password')
    var Confirm = document.getElementById('Confirm')
    var Email = document.getElementById('Email')
    var userverification = document.getElementById('userverification')

    var username_error = document.getElementById('username_error')
    var userpwd_error = document.getElementById('userpwd_error')
    var userconfirm_error = document.getElementById('userconfirm_error')
    var useremail_error = document.getElementById('useremail_error')
    var userverification_error = document.getElementById('userverification_error')

    var signupForm = document.getElementById('signupForm')

    username.onblur = check_username
    Password.onblur = check_userpwd
    Confirm.onblur = check_userconfirm
    Email.onblur = check_useremail
    userverification.onblur = check_userverification
    signupForm.onsubmit = check_myform

}


//验证用户名
function check_username(){
    pattern = /^[a-zA-Z_0-9]+$/
    var flag = true;
    var value1 = username.value.trim()
    if(value1.length==0){
        username_error.innerHTML = '用户名不能为空'
        return false;
    }else if(value1.length<6 || value1.length>10){
        username_error.innerHTML = '用户名长度必须是在6-10之间'
        return false;
    }else if(!pattern.test(value1)){
        username_error.innerHTML = '用户名只能包含字母/数字/下划线'
        return false;
    }else{
        // myajax('/fresh/check_username?username='+value1,function(){
        //     if(xmlhttp.readyState==4 && xmlhttp.status==200){
        //         ret = xmlhttp.responseText
        //         if(ret=='1'){
        //             username_error.innerHTML = '该用户已存在'
        //             return false;
        //             //document.getElementById('username_error').innerHTML = '该用户已存在'
        //         }else{
        //             document.getElementById('username_error').innerHTML = ''
        //         }
        //     }
        // })
        $.ajax({
            'type':'GET',
            'url':'/user/check_username?username='+value1,
            'success':function (value) {
                if(value == '1'){
                    $('#username_error').html('该用户已存在')
                }else{
                    $('#username_error').html('')
                }
            }
        })
    }
    return flag;
}


//验证密码,长度是6-10
function check_userpwd(){
    var flag = true;
    var value = Password.value.trim()
    if(value.length==0){
        userpwd_error.innerHTML = '密码不能为空'
        return false;
    }else if(value.length<6 || value.length>10){
        userpwd_error.innerHTML = '长度必须是在6-10之间'
        return false;
    }else{
        userpwd_error.innerHTML = ''
    }
    return flag;
}
//验证确认密码
function check_userconfirm(){
    var flag = true;
    var value = Confirm.value.trim()
    var value1 = Password.value.trim()
    if(value.length==0){
        userconfirm_error.innerHTML = '密码不能为空'
        return false;
    }else if(value != value1){
        userconfirm_error.innerHTML = '输入的密码不一致'
        return false;
    }else{
         userconfirm_error.innerHTML = ''
    }
    return flag;
}


//验证邮箱
function check_useremail(){
    var flag = true;
    myreg = /^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/
    var value = Email.value.trim()
    if(value.length==0){
        useremail_error.innerHTML = '输入不能为空'
        return false;
    }else if(!myreg.test(value)){
        useremail_error.innerHTML = '邮箱格式不正确'
        return false;
    }else{
         useremail_error.innerHTML = ''
    }
    return flag;
}


//验证验证码
function check_userverification(request){
    var flag = true;
    var value = userverification.value.trim()
    if(value.length==0) {
        userverification_error.innerHTML = '验证码不能为空'
        return false;
    }else{
        $.ajax({
            'url':'/user/check_userverification?userverification='+value,
            'type':'GET',
            'success':function (data) {
                if(data == '0'){
                    $('#userverification_error').html('验证码错误')
                }else{
                    $('#userverification_error').html('')
                }
            }
        })
    }
    return flag;
}


//验证表单
function check_myform(){
    var flag = true;
    if(!(check_username()&&check_userpwd()&&check_userconfirm()&&check_useremail()&&check_userverification())){
        flag = false
    }
    return flag;
}
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
    var Password = document.getElementById('userpwd')
    var userverification = document.getElementById('userverification')

    var username_error1 = document.getElementById('username_error1')
    var userpwd_error1 = document.getElementById('userpwd_error1')
    var userverification_error1 = document.getElementById('userverification_error1')

    var signForm = document.getElementById('signForm')

    username.onblur = check_username
    Password.onblur = check_userpwd
    userverification.onblur = check_userverification
    signForm.onsubmit = check_myform

}


//验证用户名
function check_username(){
    pattern = /^[a-zA-Z_0-9]+$/
    var flag = true;
    var value1 = username.value.trim()
    if(value1.length==0){
        username_error1.innerHTML = '用户名不能为空'
        return false;
    }else if(value1.length<6 || value1.length>10){
        username_error1.innerHTML = '用户名长度必须是在6-10之间'
        return false;
    }else if(!pattern.test(value1)){
        username_error1.innerHTML = '用户名只能包含字母/数字/下划线'
        return false;
    }else{
        $.ajax({
            'type':'GET',
            'url':'/user/check_username?username='+value1,
            'success':function (value) {
                if(value == '0'){
                    $('#username_error1').html('该用户不存在')
                }else{
                    $('#username_error1').html(' ')
                }
            }
        })
    }
    return flag;
}


//验证密码,长度是6-10
function check_userpwd(){
    var flag = true;
    var value = userpwd.value.trim()
    if(value.length==0){
        userpwd_error1.innerHTML = '密码不能为空'
        return false;
    }else if(value.length<6 || value.length>10){
        userpwd_error1.innerHTML = '长度必须是在6-10之间'
        return false;
    }else{
        $.ajax({
            'type':'GET',
            'url':'/user/check_userpwd?userpwd='+value,
            'success':function (value) {
                if(value == '0'){
                    $('#userpwd_error1').html('密码错误，请重新输入')
                }else{
                    $('#userpwd_error1').html(' ')
                }
            }
        })
    }
    return flag;
}

//验证验证码
function check_userverification(request){
    var flag = true;
    var value = userverification.value.trim()
    if(value.length==0) {
        userverification_error1.innerHTML = '验证码不能为空'
        return false;
    }else{
        $.ajax({
            'url':'/user/check_userverification?userverification='+value,
            'type':'GET',
            'success':function (data) {
                if(data == '0'){
                    $('#userverification_error1').html('验证码错误')
                }else{
                    $('#userverification_error1').html(' ')
                }
            }
        })
    }
    return flag;
}


//验证表单
function check_myform(){
    var flag = true;
    if(!(check_username()&&check_userpwd()&&check_userverification())){
        flag = false
    }
    return flag;
}
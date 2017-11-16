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

//表单验证
window.onload = function () {
    var ureceive = document.getElementById('recipients')
    var uaddress = document.getElementById('Address')
    var uzipcode = document.getElementById('postcode')
    var uphone = document.getElementById('tel')

    var ureceive_error = document.getElementById('ureceive_error')
    var uaddress_error = document.getElementById('uaddress_error')
    var uzipcode_error = document.getElementById('uzipcode_error')
    var uphone_error = document.getElementById('uphone_error')

    var signupForm = document.getElementById('signupForm')

    ureceive.onblur = check_ureceive
    uaddress.onblur = check_uaddress
    uzipcode.onblur = check_uzipcode
    uphone.onblur = check_uphone

    signupForm.onsubmit = check_myform

}


function check_ureceive(){
    var flag = true;
    var value1 = recipients.value.trim()
    if(value1.length==0){
        ureceive_error.innerHTML = '收件人不能为空'
        return false;
    }
    return flag;
}


function check_uaddress(){
    var flag = true;
    var value1 = Address.value.trim()
    if(value1.length==0){
        uaddress_error.innerHTML = '收件地址不能为空'
        return false;
    }
    return flag;
}

function check_uzipcode(){
    pattern = /^[0-9]+$/
    var flag = true;
    var value1 = postcode.value.trim()
    if(value1.length==0){
        uzipcode_error.innerHTML = '邮编不能为空'
        return false;
    }else if(value1.length != 6) {
        uzipcode_error.innerHTML = '邮编为6位数字'
        return false;
    }
    return flag;
}

function check_uphone(){
    pattern = /^[0-9]+$/
    var flag = true;
    var value1 = tel.value.trim()
    if(value1.length==0){
        uphone_error.innerHTML = '手机号码不能为空'
        return false;
    }else if(value1.length != 11 & !pattern.test(value1)) {
        uphone_error.innerHTML = '手机号码为11位数字'
        return false;
    }
    return flag;
}

//验证表单
function check_myform(){
    var flag = true;
    if(!(check_uaddress()&&check_ureceive()&&check_uzipcode()&&check_uphone())){
        flag = false
    }
    return flag;
}
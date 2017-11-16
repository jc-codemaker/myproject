
// 删除商品
function cart_del(cart_id) {
    var del = confirm('确认删除该商品？');
    if(del){
        $.get('/shopping_cart/delete'+ cart_id,function (data) {
            if (data.flag == 1){
                $('ul').remove('#'+cart_id);
                total();
            }
        })
    }
    return false;
}

//　计算小计和合计
function total() {
    var total1 = 0;
    var total_count = 0;
    $('.col07').each(function () {
        // 获取输入框中商品的数量
        // prev() 获得匹配元素集合中每个元素紧邻的前一个同胞元素
        var count = $(this).prev().find('input').val();
        //　获取商品单价
        var price = $(this).prev().prev().text();
        //  计算小计,结果保留两位小数
        var total0 = parseFloat(count)*parseFloat(price);
        $(this).text(total0.toFixed(2))
        //  判断当前商品是否被勾选
        //  siblings() 获得匹配集合中每个元素的同胞
        //  children() 方法返回返回被选元素的所有直接子元素
        //  prop() 方法设置或返回被选元素的属性和值

        if ($(this).siblings('.col01').children('input').prop('checked')){
            total1 += total0;
            total_count+=parseInt(count);
        }
    });
    $('#total').text(total1.toFixed(2));
    $('.total_count1').text(total_count);
}

$(function () {
    total();

    // 全选
    $('#check_all').click(function () {
        var state = $(this).prop('checked');
        $(':checkbox:not(#check_all)').prop('checked',state);
        total();
    });

    // 选择
    $(':checkbox:not(#check_all)').click(function () {
        if ($(this).prop('checked')){
            if($(':checked').length+1==$(':checkbox').length){
                $('#check_all').prop('checked',true);
            }
        }else {
            $('#check_all').prop('checked',false);
        }
        total();
    });

    //  数量加
    $('.add').click(function () {
        var txt = $(this).next();
        var count = parseInt(txt.val());
        txt.val(count+1).blur();
    });

    //　　数量减
    $('.minus').click(function () {
        var txt = $(this).prev();
        var count = parseInt(txt.val());
        if(count<=1){
            txt.val(1).blur();
        }else {
            txt.val(count-1).blur();
        }
    });

    $('.num_show').blur(function () {
        var count=parseInt($(this).val());
        if (count<=0){
            $(this).val(1);
        }else if(count>=100){
            $(this).val(100);
            alert('单次购买数量不能超过100')
        }
        cart_id = $(this).parents('.cart_list_td').attr('id')

        $.get('/shopping_cart/edit'+cart_id+'_'+count,function (data) {
            if(data.flag == 1){
                total();
            }else {
                $(this).val(data.flag);
            }
        })
    });
});
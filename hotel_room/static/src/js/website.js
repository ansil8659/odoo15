// ADDING PRODUCT
odoo.define('hotel_room.booking',function(require){
'use strict';

var ajax = require('web.ajax');
$(function(){

$('#save').on('click', function () {
    var product_name = $('#product_name').val();
    var price = $('#price').val();
    var count = $('#myTable tr').length;
    console.log(price);
    if (price != "") {
        $('#myTable tbody').append('<tr class="child"><td>' + count + '</td><td data-p_rate=' +price+ '>' + product_name + '</td><td>' + price + '</td><td><a href="javascript:void(0);" class="remCF1 btn btn-small bg-transparent text-primary"><i class="fa-regular fa-trash-can"></i></a></td></tr>');
    }

    // SHOWING PRODUCTS ON SELECT BOX
    var item_options = [];
    var selection = "<option size="+1+"value="+0+">Select Product</option>";
    $('#myTable tbody tr td:nth-child(2)').each(function () {
        item_options.push('<option data-rate='+ $(this).attr('data-p_rate')+' value=' + $(this).text() + '>' + $(this).text() + '</option>');

    });

    $('#productId').empty().append(selection);
    $('#productId').append(item_options.join());
});

});

});
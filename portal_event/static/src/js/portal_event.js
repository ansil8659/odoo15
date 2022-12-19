odoo.define('portal_event.event', function (require) {
"use strict";
var session = require('web.session')
$(document).ready(function() {
        $('.toggle_event').on('click', function(e){
       var value_id=$(this).data('id')
            $(`#${value_id}`).toggleClass("d-none")z
            console.log(1234567,'qwert')
        });
    });
});

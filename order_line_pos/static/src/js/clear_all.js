/** @odoo-module*/
odoo.define('pos_delete_orderline.DeleteOrderLinesAll', function(require) {
'use strict';
   const PosComponent = require('point_of_sale.PosComponent');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require("@web/core/utils/hooks");
   const Registries = require('point_of_sale.Registries');
   class OrderLineClearALL extends PosComponent {
       setup() {
           super.setup();
           useListener('click', this.onClick);
       }
      async onClick() {
                        var order = this.env.pos.get_order();
                        var lines = order.get_orderlines();
                        console.log("fxzdfgh", lines)
                        order.remove_orderline(lines);
       }
   }

   OrderLineClearALL.template = 'OrderLineClearALL';
   ProductScreen.addControlButton({
       component: OrderLineClearALL,
       condition: function() {
           return this.env.pos;
       },
   });
   Registries.Component.add(OrderLineClearALL);
   return OrderLineClearALL;
});
	

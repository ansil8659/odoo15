odoo.define('point_of_sale.PurchaseLimitPOS', function (require) {
    "use strict";

        const ProductScreen = require('point_of_sale.ProductScreen');
        const Registries = require('point_of_sale.Registries');
        const {Gui} = require('point_of_sale.Gui')
        var models = require('point_of_sale.models');
        models.load_fields('res.partner', 'purchase_limit');
        models.load_fields('res.partner', 'limit_amount');
        const PurchaseLimitPOS = (ProductScreen) =>
        class extends ProductScreen {
            async _onClickPay() {
                const customer = this.currentOrder.get_client();
                const amount = this.currentOrder.get_total_with_tax();
                console.log("customer---" ,customer)

                if (!customer){
                    console.log('asdfgh');
                    Gui.showPopup('ErrorPopup',{
                         'title': ('Error: Payment Validation Error'),
                         'body': ('Must Be Select a Customer')
                          });
                    }
                    else{
                        if (customer.purchase_limit == true){
                            if (customer.limit_amount < amount){
                                Gui.showPopup('ErrorPopup',{
                                                         'title': ('Error: Payment Validation Error'),
                                                         'body': ('Purchase Limit Of ' + customer.name + ' is ' + customer.limit_amount)
                                                     });

                            }
                             else{
                          await super._onClickPay()
                        }
                        }

                    }

            }

        }


      Registries.Component.extend(ProductScreen, PurchaseLimitPOS);
      return ProductScreen;
  });

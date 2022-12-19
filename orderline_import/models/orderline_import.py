from odoo import models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def import_line(self):
        return {

            'name': _('Order Line'),

            'type': 'ir.actions.act_window',

            'res_model': 'order.line.wizard',

            'view_mode': 'form',
            # 'res_id': wizard.id,
            'target': 'new'
        }

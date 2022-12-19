from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_discount_limit_amount = fields.Float("Discount Limit", readonly=False, default=200)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'disc_limit.so_discount_limit_amount', self.so_discount_limit_amount)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            so_discount_limit_amount=params.get_param('disc_limit.so_discount_limit_amount')
        )
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total = fields.Float("total", compute='disc_limit')

    @api.onchange('order_line')
    def disc_limit(self):
        orders_disc_sum = 0
        today = fields.date.today()
        first_day = fields.date.today().replace(day=1)
        discount_limit = float(self.env['ir.config_parameter'].sudo().get_param('disc_limit.so_discount_limit_amount'))
        orders = self.env['sale.order'].search(
            [('state', '=', 'sale'), ('date_order', '>=', first_day), ('date_order', '<=', today)])
        for record in orders.order_line:
            orders_disc = record.price_unit * record.discount / 100
            orders_disc_sum = orders_disc_sum + orders_disc

        order_line_disc_sum = 0
        for rec in self.order_line:
            order_line_disc = rec.price_unit * rec.discount / 100
            order_line_disc_sum = order_line_disc_sum + order_line_disc

        total_discount = orders_disc_sum + order_line_disc_sum

        if total_discount > discount_limit:
            self.update(
                {'order_line': False})
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'Discount crossed the limit'
                }
            }

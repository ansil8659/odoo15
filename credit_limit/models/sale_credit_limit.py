from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Boolean("Credit Limit")
    warn_amount = fields.Float("Warning Amount")
    block_amount = fields.Float("Blocking Amount")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    due_amount = fields.Float("Due Amount", readonly=True)
    is_warning = fields.Integer(default=1)
    warn = fields.Float("warning")

    @api.onchange('partner_id')
    def amount_due(self):
        customer = self.partner_id.id
        amount = self.env['account.move'].search([('partner_id', '=', customer), ('payment_state', '=', 'not_paid')])
        total = 0
        for rec in amount:
            total = total + rec.amount_total_signed
        self.due_amount = total

    @api.onchange('order_line')
    def limit_credit(self):
        customer = self.partner_id.id
        amount = self.env['account.move'].search([('partner_id', '=', customer), ('payment_state', '=', 'not_paid')])
        total = 0
        for rec in amount:
            total = total + rec.amount_total_signed
        warning = self.partner_id.warn_amount
        self.warn = warning
        print(self.warn)
        blocking = self.partner_id.block_amount
        limit = self.partner_id.credit_limit
        if limit == 1:
            print("kkk")
            if warning == 0:
                print(1)
            else:
                if warning <= total < blocking:
                    self.is_warning = 0
                else:
                    self.is_warning = 1
            if warning == 0:
                print(1)
            else:
                if total >= blocking:
                    self.update(
                        {'order_line': False, 'partner_id': False})
                    return {
                        'warning': {
                            'title': 'Warning',
                            'message': 'Credit Limit Is Crossed'
                        }
                    }

    @api.onchange('order_line')
    def courses(self):
        x = self.env['slide.channel'].search([])
        for rec in x:
            print(rec.name)
        # print(x.name)

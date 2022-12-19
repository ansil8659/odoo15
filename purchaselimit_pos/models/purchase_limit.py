from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    purchase_limit = fields.Boolean("Purchase Limit")
    limit_amount = fields.Float("Limit Amount")

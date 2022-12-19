from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    spanish_name = fields.Char("sp.Name")

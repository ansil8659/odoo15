from odoo import models, api


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    # @api.onchange('slide_ids')
    # def courses(self):
    #     print(self.name)

from datetime import datetime

from odoo import models, fields


class University(models.Model):
    _name = 'university.show'
    _rec_name = 'u_name'

    u_name = fields.Char('Name')
    u_code = fields.Char('Code')
    u_type = fields.Char('Type')


class UniversityEvent(models.Model):
    _name = 'university.event'
    _rec_name = 'e_name'

    e_name = fields.Char('Name')
    e_type = fields.Char('Type')
    start_date = fields.Date("From")
    end_date = fields.Date("To")
    current_date = fields.Date(default=datetime.today())
    u_name_id = fields.Many2one('university.show')
    u_code = fields.Char(related='u_name_id.u_code')
    u_type = fields.Char(related='u_name_id.u_type')
    state = fields.Selection(string='Status',
                             selection=[('draft', 'Draft'), ('ongoing', 'OnGoing'), ('expires', 'Expired')],
                             default='draft')
    slot_ids = fields.One2many('event.slot', 'e_name_id')


class EventSlot(models.Model):
    _name = 'event.slot'

    time = fields.Datetime("Time")
    content = fields.Char('Content')
    e_name_id = fields.Many2one('university.event')

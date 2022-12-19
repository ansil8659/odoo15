from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


class HotelRoom(models.Model):
    _name = "hotel.room"
    _rec_name = 'room_no'
    room_no = fields.Char("RoomNo", required=True)
    bed = fields.Selection(
        string='Bed',
        selection=[('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')],
        help="used to select the Bed type"
    )
    rent = fields.Monetary("Rent")
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)

    facility_ids = fields.Many2many("room.facility", string="Facility")
    available_bed = fields.Integer("Available Beds")
    state = fields.Selection(string='Status',
                             selection=[('available', 'Available'), ('not_available', 'Not Available')],
                             copy=False, index=True, tracking=3, default='available')


class RoomFacility(models.Model):
    _name = "room.facility"
    _rec_name = 'facility'
    facility = fields.Char("Facility")


class RoomAccommodation(models.Model):
    _name = "room.accommodation"
    _inherit = 'mail.thread'
    _rec_name = "name"
    _order = 'check_in desc'
    # _rec_name = "facilities"
    name = fields.Char(required=True, index=True, copy=False,
                       readonly=True, default='New')
    partner_id = fields.Many2one(
        'res.partner', string='Guest',
        required=True, change_default=True, index=True, tracking=1,
    )
    no_of_guest = fields.Integer("No.Guest")
    check_in = fields.Datetime("Check-In", readonly=True)
    check_out = fields.Datetime("Check-Out", readonly=True)
    expected_days = fields.Integer("Expected Days")
    # expected_days_test = fields.Date('test', compute='_expected_date_test')
    expected_date = fields.Date("Expected Date", compute='_expected_date', readonly=True, store=True)
    current_date = fields.Date(default=datetime.today())
    active = fields.Boolean(string="Active", default=True)
    bed_type = fields.Selection(
        string='Bed Type',
        selection=[('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')],
        help="used to select the Bed type"
    )
    facility_ids = fields.Many2many("room.facility", string="Facility")

    room_id = fields.Many2one("hotel.room", string="Room", domain=[('state', '=', 'available')])
    status = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'), ('check-in', ' Check-In'), ('check-out', ' Check-Out'), ('cancel', 'Cancel')],
        copy=False, index=True, tracking=3, default='draft'
    )
    guest_info_ids = fields.One2many("guest.info", "accommodation_id")
    payment_ids = fields.One2many('room.accommodation.payment', 'payment_id')
    invoice_id = fields.Many2one('account.move')
    total = fields.Float(string="Total", compute='_compute_total')
    paid = fields.Boolean("Paid", compute='compute_ribbon')

    @api.depends('payment_ids.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.total = sum(rec.mapped('payment_ids').mapped('subtotal'))

    @api.depends('expected_days')
    def _compute_rent(self):
        print(self.room_id.rent)
        # for record in self:
        #     record.rent_payment = record.expected_days * self.room_id.rent

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'room.accommodation') or 'New'
        result = super(RoomAccommodation, self).create(vals)
        return result

    def change_stage_check_in(self):
        attachment_id = self.message_main_attachment_id.id
        total_guest = self.guest_info_ids
        print(attachment_id)
        print(self.room_id.rent)
        print(self.expected_days)
        print(self.room_id)
        if self.no_of_guest == len(total_guest) and attachment_id != False:
            print(attachment_id)
            for rec in self:
                rec.status = 'check-in'
                rec.room_id.state = 'not_available'
            self.check_in = datetime.today()
        else:
            return {
                'type': 'ir.actions.client', 'tag': 'display_notification',
                'params': {
                    'title': _('Warning..'),
                    'message': 'Pls attach the files // Please provide all guest details',
                    'sticky': False,
                }
            }
        for record in self:
            if record.check_in:
                date1 = datetime.strftime(record.check_in, "%Y-%m-%d %H:%M:%S")
                date2 = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S") + relativedelta(days=+ record.expected_days)
                record.expected_date = date2
                print(date2)
            else:
                record.expected_date = record.check_in

        pay = self.env['room.accommodation.payment'].create({
            'payment_id': self.id,
            'payment_no_id': self.env.context.get("default_name"),
            'description': self.room_id.room_no,
            'quantity': self.expected_days,
            'unit_price': self.room_id.rent
        })
        print(pay)
        return pay

    def change_stage_check_out(self):
        # print(self.room_id.rent)
        self.status = 'check-out'
        if self.status == 'check-out':
            for rec in self:
                rec.status = 'check-out'
                rec.room_id.state = 'available'
        self.check_out = datetime.today()
        a = self.name
        print(a)
        accmmtn_id = self.name
        data = self.env['room.accommodation.payment'].search([('payment_id', '=', accmmtn_id)])
        lst = []
        for rec in data:
            lists = {
                'product_id': rec.id,
                'name': rec.description,
                'quantity': rec.quantity,
                'price_unit': rec.unit_price,
                'price_subtotal': rec.subtotal,
            }
            lst.append(lists)
        self.invoice_id = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.context_today(self),
            'partner_id': self.partner_id.id,
            # 'currency_id': self.currency_id.id,
            # 'amount_total': self.delivery_total,
            'invoice_line_ids': lst
        })
        return {
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.invoice_id.id,
            'target': 'self',
            # 'context': {
            #     'default_fee': data.unit_price,
            # }
        }

    print("1221212121212121212121")

    @api.depends('invoice_id.payment_state')
    def compute_ribbon(self):
        if self.invoice_id.payment_state == 'paid':
            self.paid = True
        else:
            self.paid = False

    def change_stage_check_cancel(self):
        self.status = 'cancel'
        if self.status == 'cancel':
            for rec in self:
                rec.status = 'cancel'
                rec.active = False

    def hotel_report_view(self):
        return {

            'name': _('Hotel Report'),

            'type': 'ir.actions.act_window',

            'res_model': 'hotel.report.wizard',

            'view_mode': 'form',

            'target': 'new'
        }

    # def hotel_report_excel(self):
    #     return {'type': 'ir.actions.report', 'report_type': 'XLSX',
    #             'data': {'model': 'Wizard model', 'output_format': 'XLSX',
    #                      'options': json.dumps(data, default=date_utils.json_default),
    #                      'report_name': 'Excel Report Name', }, }

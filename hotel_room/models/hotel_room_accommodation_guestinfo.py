from datetime import datetime

from odoo import models, fields, api


class GuestInfo(models.Model):
    _name = "guest.info"
    _rec_name = "accommodation_id"
    accommodation_id = fields.Many2one("room.accommodation", readonly=True)
    guest = fields.Char(string="Guest")
    age = fields.Integer("Age")
    gender = fields.Selection(string='Gender',
                              selection=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])


class RoomOrderFood(models.Model):
    _name = "room.order.food"
    _rec_name = 'order_no'

    order_no = fields.Char(required=True, index=True, copy=False,
                           readonly=True, default='New')
    room_id = fields.Many2one("hotel.room", domain="[('state','=','not_available')]")
    guest_ids = fields.Many2many("guest.info")
    order_date = fields.Datetime(default=datetime.today())
    guest = fields.Many2one("room_accommodation")
    category_ids = fields.Many2many("room.order.food.category")
    item_ids = fields.Many2many("room.order.food.item")
    list_no_ids = fields.One2many('room.order.food.item.list', 'list_no_id')
    list_total = fields.Float(string="Total", compute='_compute_total')

    @api.depends('list_no_ids.list_subtotal')
    def _compute_total(self):
        for rec in self:
            rec.list_total = sum(rec.mapped('list_no_ids').mapped('list_subtotal'))
        # print(self.list_total)

    @api.onchange('room_id')
    def show_items(self):
        a = self.item_ids
        print(a)
        b = self.room_id
        print(b.id)
        data = self.env['room.accommodation'].search([('room_id', '=', b.room_no), ('status', '=', "check-in")])
        for rec in data.guest_info_ids:
            self.update(
                {'guest_ids': [
                    (4, rec.id)
                ]}
            )

        print(data)

    @api.onchange('category_ids')
    def show_food_items(self):
        for record in self:
            record.item_ids = record.category_ids.cat_ids

    @api.model
    def create(self, vals):
        if vals.get('order_no', 'New') == 'New':
            vals['order_no'] = self.env['ir.sequence'].next_by_code(
                'order_no') or 'New'
        result = super(RoomOrderFood, self).create(vals)
        return result


class RoomOrderFoodCategory(models.Model):
    _name = "room.order.food.category"
    _rec_name = 'category'

    category = fields.Char("Category")
    cat_ids = fields.One2many('room.order.food.item', 'category_id', invisible=True)


class RoomOrderFoodItems(models.Model):
    _name = "room.order.food.item"
    # _rec_name = 'name'

    image = fields.Image("Image")
    name = fields.Char(required=True, index=True, copy=False,
                       readonly=True, default='New')
    item = fields.Char("Name")
    category_id = fields.Many2one("room.order.food.category")
    price = fields.Float("Price")
    quantity = fields.Float("Quantity")
    description = fields.Html("Description")
    item_no_id = fields.Many2one("room.order.food")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'name') or 'New'
        result = super(RoomOrderFoodItems, self).create(vals)
        return result

    def add_to_list(self):
        self.env['room.order.food.item.list'].create({
            'list_no_id': self.env.context.get("default_name"),
            'list_name': self.item,
            'list_description': self.description,
            'list_category': self.category_id.category,
            'list_price': self.price,
            'list_quantity': self.quantity
        })
        order_id = self.env.context.get("default_name")
        main = self.env['room.order.food'].search([('id', '=', order_id)])
        print(main.room_id.id)
        local = self.env['room.accommodation'].search([('room_id', '=', main.room_id.id)])
        print(local.id)

        self.env['room.accommodation.payment'].create({
            'payment_id': local.id,
            'payment_no_id': self.env.context.get("default_name"),
            'description': self.item,
            'quantity': self.quantity,
            'unit_price': self.price
        })


class RoomOrderFoodItemsList(models.Model):
    _name = "room.order.food.item.list"

    list_no_id = fields.Many2one("room.order.food")
    list_name = fields.Char("Name")
    list_category = fields.Char("Category")
    list_price = fields.Float("Price")
    list_quantity = fields.Float("Quantity")
    list_description = fields.Text("Description")
    list_subtotal = fields.Float("Subtotal", compute='_compute_subtotal')
    list_total = fields.Float("Total", compute='_compute_total')

    @api.depends('list_quantity', 'list_price')
    def _compute_subtotal(self):
        for record in self:
            record.list_subtotal = record.list_quantity * record.list_price


class RoomAccommodationPayment(models.Model):
    _name = "room.accommodation.payment"

    payment_no_id = fields.Many2one("room.order.food")
    payment_id = fields.Many2one('room.accommodation')
    description = fields.Text("Description")
    quantity = fields.Float("Quantity")
    uom = fields.Many2one('uom.uom')
    unit_price = fields.Float("Unit Price")
    subtotal = fields.Float("Subtotal", compute='_compute_subtotal')

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.unit_price


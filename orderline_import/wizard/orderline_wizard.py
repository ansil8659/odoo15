from odoo import models, fields
import xlrd
import base64

from odoo.exceptions import UserError


class OrderLineWizard(models.Model):
    _name = 'order.line.wizard'

    wizard_import = fields.Binary(string="File")

    def action_done(self):
        try:
            book = xlrd.open_workbook(file_contents=(base64.decodebytes(self.wizard_import)))
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        for sheets in book.sheets():
            for rows in range(sheets.nrows):
                if rows >= 1:
                    row_values = sheets.row_values(rows)
                    active_order = self.env['sale.order'].browse(self.env.context.get('active_ids'))
                    prdct_id = row_values[0]
                    uom_id = str(row_values[3])
                    s = len(row_values)-1
                    print(s)
                    # print(uom_id)
                    # print(prdct_id)
                    main = self.env['product.product'].search([('product_tmpl_id.name', '=', prdct_id), ('product_tmpl_id.uom_id.name', '=', uom_id)])
                    lists = []
                    for rec in main:
                        print(rec.id)
                        print(rec.product_tmpl_id.uom_id.id)
                        if not active_order.order_line:
                            # print(row_values)

                            self.env['sale.order.line'].create({
                                'product_id': rec.id,
                                'name': row_values[1],
                                'product_uom_qty': int(row_values[2]),
                                'product_uom': rec.product_tmpl_id.uom_id.id,
                                'price_unit': row_values[4],
                                'order_id': int(active_order)
                            })
                        else:
                            main_a = self.env["sale.order.line"].search([('product_id', '=', rec.id),
                                                                         ('order_id', '=', self._context.get('active_id'))])
                            if main_a:
                                # print(main_a.product_uom_qty)
                                main_a.write({
                                    'product_uom_qty': main_a.product_uom_qty + int(row_values[2]),
                                })
                            else:
                                self.env['sale.order.line'].create({
                                    'product_id': rec.id,
                                    'name': row_values[1],
                                    'product_uom_qty': int(row_values[2]),
                                    'product_uom': rec.product_tmpl_id.uom_id.id,
                                    'price_unit': row_values[4],
                                    'order_id': int(active_order)
                                })

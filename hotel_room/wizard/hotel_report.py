import io
import xlsxwriter
from odoo import models, fields
from odoo.tools.safe_eval import json


class HotelReportWizard(models.TransientModel):
    _name = 'hotel.report.wizard'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    partner_id = fields.Many2one('res.partner', string="Guest")

    def report_hotel(self):
        query = """select a.name,check_in,check_out,status from room_accommodation join res_partner a on partner_id = 
        a.id """
        if self.date_from:
            from_date = """ where check_in >= '%s' """ % self.date_from
            query += from_date
        if self.date_to:
            to_date = """ and check_in <= '%s' """ % self.date_to
            query += to_date
        if self.partner_id:
            partner = """ and a.id = '%s' """ % self.partner_id.id
            query += partner
        self.env.cr.execute(query)
        room_query = self.env.cr.dictfetchall()
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner': self.partner_id,
            'query': room_query
        }
        return self.env.ref('hotel_room.action_report_hotel_management').report_action(self, data=data)

    def print_xlsx(self):
        queries = """select a.name,check_in,check_out,status from room_accommodation join res_partner a on partner_id 
        = a.id """
        if self.date_from:
            from_date = """ where check_in >= '%s' """ % self.date_from
            queries += from_date
        if self.date_to:
            to_date = """ and check_in <= '%s' """ % self.date_to
            queries += to_date
        if self.partner_id:
            partner = """ and a.id = '%s' """ % self.partner_id.id
            queries += partner
        self.env.cr.execute(queries)
        room_queries = self.env.cr.dictfetchall()
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner': self.partner_id,
            'query': room_queries
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'hotel.report.wizard',
                     'options': json.dumps(data, default=fields.date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        sheet.merge_range('A1:F2', 'Hotel Management Report', head)
        header = workbook.add_format({'align': 'cent', 'bold': True, 'font_size': '10px'})
        date = workbook.add_format({'bold': True})
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        if data['date_from']:
            sheet.write(4, 0, 'From', date)
            sheet.write(4, 1, data['date_from'])
        if data['date_to']:
            sheet.write(5, 0, 'To', date)
            sheet.write(5, 1, data['date_to'])
        row = 6
        col = 0
        sheet.write(row, col, 'SL.No', header)
        sheet.write(row, col + 1, 'Guest', header)
        sheet.write(row, col + 2, 'Check-In', header)
        sheet.write(row, col + 3, 'Check-Out', header)
        sheet.write(row, col + 4, 'State', header)
        rows = 6
        cols = 0
        sl_no = 0
        values = data.get('query')
        for rec in values:
            rows = rows + 1
            sl_no = sl_no + 1
            sheet.write(rows, cols, sl_no)
            sheet.write(rows, cols + 1, rec.get('name'))
            sheet.write(rows, cols + 2, rec.get('check_in'))
            sheet.write(rows, cols + 3, rec.get('check_out'))
            sheet.write(rows, cols + 4, rec.get('status'))
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

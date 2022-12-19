from odoo import http
from odoo.http import request
import requests
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteMail(WebsiteSale):
    @http.route(['/shop/confirmation'], type="http", auth="public", website=True)
    def shop_payment_confirmation(self, **post):
        res = super(WebsiteMail, self).shop_payment_confirmation(**post)
        admin = request.env['res.users'].search([]).filtered(lambda ml: ml.has_group('sales_team.group_sale_manager'))
        # if admin.has_group('sales_team.group_sale_manager'):
        admins = []
        for i in admin:
            print(i.login)
            admins.append(i.login)
        for dec in admin:
            print(dec.login)
            email_values = {
                'email_to': dec.login,
                'email_cc': False,
                'auto_delete': True,
                'recipient_ids': [],
                'partner_ids': [],
                'scheduled_date': False,
            }
            print(email_values)

        print(admin)
        # print(requests.session())
        # qwert = request.env['sale.order'].sudo().search(['id', '=', request.session.get('sale_last_order_id')])
        session = request.session.get('sale_last_order_id')
        print(session)
        order = request.env['sale.order'].sudo().search([], limit=1)
        print(order.id)
        if order.id == session:
            # print(order.website_url)
            template = request.env.ref('website_mail_snd.email_template_website')
            template.sudo().send_mail(order.id, force_send=True, email_values=email_values)
        # return request.render("website_mail_snd.tmp_shop_form_success", {})
        return res

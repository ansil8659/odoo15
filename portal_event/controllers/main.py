from odoo import http, fields
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalEvent(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        main = super()._prepare_home_portal_values(counters)
        u_event_count = request.env['university.event'].search_count([('start_date', '>', fields.Date.today())])
        main['u_event_count'] = u_event_count
        return main

    @http.route(['/my/events'], type="http", auth="user", website=True)
    def u_event(self):
        values = self._prepare_portal_layout_values()
        events = request.env['university.event'].search([('start_date', '>', fields.Date.today())])
        # lists = []
        # for rec in events.slot_ids:
        #     print(rec.time)
        #     print(rec.content)
        #     print(rec.website_url)
        #     each = {
        #         'name': rec.e_name,
        #         'from': rec.start_date,
        #         'to': rec.end_date,
        #     }
        #     lists.append(each)
        # print(lists)
        values.update({
            'value': events,
            'slot': events.slot_ids,
            'page_name': 'events',
            'default_url': '/my/invoices',

        })

        return request.render("portal_event.portal_my_events", values)

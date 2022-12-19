# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    @http.route(['/hotel/'], type='http', auth="user", website=True)
    def hotel(self):
        accommodation = request.env['room.accommodation'].sudo().search([])
        partners = request.env['res.partner'].sudo().search([])
        rooms = request.env['hotel.room'].sudo().search([])
        values = {}
        values.update({
            'accommodation': accommodation,
            'partners': partners,
            'rooms': rooms,
        })
        return request.render("hotel_room.online_booking_form", values)

    @http.route(['/hotel/submit/'], type='http', auth="user", website=True)
    def hotel_submit(self, **post):
        partner = post['partner_id']
        print(partner)
        guest = request.httprequest.form.getlist('guest')
        guest_list = []
        for rec in guest:
            guests = request.env['res.partner'].search([('id', '=', rec)])
            lists = request.env['guest.info'].sudo().create({
                'guest': guests.name
            })
            guest_list.append(lists.id)
        print(guest_list)
        accommodation = request.env['room.accommodation'].sudo().create({
                    'partner_id': post.get('partner_id'),
                    'room_id': post.get('room_id'),
                    'expected_days': post.get('expected_days'),
                    'check_in': post.get('check_in'),
                    'guest_info_ids': guest_list,
                    'no_of_guest': post.get('no_of_guest')
        })
        vals = {
                    'accommodation': accommodation,
                }
        return request.render("hotel_room.tmp_hotel_form_success", vals)

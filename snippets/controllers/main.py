from odoo import http
from odoo.http import request


class WebsiteSnippet(http.Controller):
    @http.route(['/eLearning'], type="json", auth="public", website=True)
    def course(self):
        course = request.env['slide.channel'].search([], limit=3, order='create_date desc')
        lists = []
        for rec in course:
            print(rec.name)
            print(rec.website_url)
            each = {
                'img': rec.image_1920,
                'name': rec.name,
                'url': rec.website_url,
                'description': rec.description_short
            }
            lists.append(each)
        data = {
            'value': lists
        }
        res = http.Response(template='snippets.basic_snippet', qcontext=data)
        return res.render()

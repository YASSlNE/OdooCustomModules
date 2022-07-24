# -*- coding: utf-8 -*-
# from odoo import http


# class ExempleModule2(http.Controller):
#     @http.route('/exemple_module2/exemple_module2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exemple_module2/exemple_module2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exemple_module2.listing', {
#             'root': '/exemple_module2/exemple_module2',
#             'objects': http.request.env['exemple_module2.exemple_module2'].search([]),
#         })

#     @http.route('/exemple_module2/exemple_module2/objects/<model("exemple_module2.exemple_module2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exemple_module2.object', {
#             'object': obj
#         })

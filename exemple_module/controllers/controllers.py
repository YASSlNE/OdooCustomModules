# -*- coding: utf-8 -*-
# from odoo import http


# class ExempleModule(http.Controller):
#     @http.route('/exemple_module/exemple_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exemple_module/exemple_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exemple_module.listing', {
#             'root': '/exemple_module/exemple_module',
#             'objects': http.request.env['exemple_module.exemple_module'].search([]),
#         })

#     @http.route('/exemple_module/exemple_module/objects/<model("exemple_module.exemple_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exemple_module.object', {
#             'object': obj
#         })

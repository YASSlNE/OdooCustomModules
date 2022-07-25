# -*- coding: utf-8 -*-
# from odoo import http


# class Clinique(http.Controller):
#     @http.route('/clinique/clinique/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/clinique/clinique/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('clinique.listing', {
#             'root': '/clinique/clinique',
#             'objects': http.request.env['clinique.clinique'].search([]),
#         })

#     @http.route('/clinique/clinique/objects/<model("clinique.clinique"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('clinique.object', {
#             'object': obj
#         })

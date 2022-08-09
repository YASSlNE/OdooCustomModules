# -*- coding: utf-8 -*-
# from odoo import http


# class OrdreDeMission(http.Controller):
#     @http.route('/ordre_de_mission/ordre_de_mission/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ordre_de_mission/ordre_de_mission/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ordre_de_mission.listing', {
#             'root': '/ordre_de_mission/ordre_de_mission',
#             'objects': http.request.env['ordre_de_mission.ordre_de_mission'].search([]),
#         })

#     @http.route('/ordre_de_mission/ordre_de_mission/objects/<model("ordre_de_mission.ordre_de_mission"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ordre_de_mission.object', {
#             'object': obj
#         })

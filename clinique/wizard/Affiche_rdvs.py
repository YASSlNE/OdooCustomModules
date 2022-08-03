# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AfficheRdvs(models.TransientModel):
    _name = 'clinique.rdvs.affiche'
    _description = 'Affichage des rendez vous sous forme pdf'
    docteur_id = fields.Many2one('clinique.docteur')
    _inherit = 'clinique.rdv'
    def action_print_rdvs(self):
        # print(docteur_id)
        data = self.env['clinique.rdv'].search([('docteur', '=', 'self.docteur_id')])
        for d in data:
            print(d['date'])
            print('mlsqdkjfqsdmlkfjqs')
        return None
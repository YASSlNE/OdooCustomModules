# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AfficheRdvs(models.TransientModel):
    _name = 'clinique.rdvs.affiche'
    _description = 'Affichage des rendez vous sous forme pdf'
    docteur_id = fields.Many2one('clinique.docteur', 'Docteur')

    def action_print_rdvs(self):
        data = self.env['clinique.rdvs.affiche'].browse(self.env.context.get('active_ids'))
        print(data)
        return None
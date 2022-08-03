# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AfficheRdvs(models.TransientModel):
    _name = 'clinique.rdvs.affiche'
    _description = 'Affichage des rendez vous sous forme pdf'
    docteur_id = fields.Many2one('clinique.docteur')
    date = fields.Date('Date', default=fields.Datetime.now)
    def action_print_rdvs(self):
        data = self.env['clinique.rdv'].search(['&', '&', ('docteur', '=', self.docteur_id.id), ('state', '=', 'confirmation'), ('date', '=', self.date)])
        for d in data:
            print(d.patient.name)
        return None
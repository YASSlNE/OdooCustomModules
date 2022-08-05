# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta

class AfficheRdvs(models.TransientModel):
    _name = 'clinique.rdvs.affiche'
    _description = 'Affichage des rendez vous sous forme pdf'
    docteur_id = fields.Many2one('clinique.docteur')
    date = fields.Datetime('Date', default=fields.Datetime.now)


    def action_print_rdvs(self):
        # patients = []
        # for d in data:
        #     patients.append(d.patient.name)
        # print(type(docs))
        # names = []
        # print(docs.patient.name)
        # for patient in docs.patient:
        #     names.append({'nom': patient.name})
        # data = {
        #     'ids': self.ids,
        #     'names': names,
        # }
        start_date = self.date
        end_date = self.date+timedelta(hours=23, minutes=59, seconds=59)
        print(end_date)
        data = {
            'ids': self.ids,
            'form': {
                'docteur_id': self.docteur_id.id,
                'start_date': start_date,
                'end_date': end_date,
            },
        }
        return self.env.ref('clinique.action_report_rdvs').report_action(self, data)

class AfficheRdvsPDF(models.AbstractModel):
    _name = 'report.clinique.report_rdvs'
    def _get_report_values(self, docids, data):
        print(data['form'])
        docs = self.env['clinique.rdv'].search(['&', '&', '&', ('docteur', '=', int(data['form']['docteur_id'])), ('state', '=', 'confirmation'), ('date', '<=', data['form']['end_date']), ('date', '>=', data['form']['start_date'])])
        # docs = self.env['clinique.rdv'].browse(1)#(['&', '&', ('docteur', '=', data['form']['docteur_id']), ('state', '=', 'confirmation'), ('date', '=', data['form']['date'])])
        print(docs)
        # docs = data["names"]
        # print(type(docs['form']['docs']))
        # print(type(docs))
        # print('mslqfkjmqsdlkfj')
        return {
                   'doc_ids': docids,
                   'doc_model': 'clinique.rdv',
                   'docs': docs,
            }

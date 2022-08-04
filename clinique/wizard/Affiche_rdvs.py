# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AfficheRdvs(models.TransientModel):
    _name = 'clinique.rdvs.affiche'
    _description = 'Affichage des rendez vous sous forme pdf'
    docteur_id = fields.Many2one('clinique.docteur')
    date = fields.Date('Date', default=fields.Datetime.now)


    def action_print_rdvs(self):
        # patients = []
        # for d in data:
        #     patients.append(d.patient.name)
        # print(type(docs))
        names = []
        # print(docs.patient.name)
        # for patient in docs.patient:
        #     names.append({'nom': patient.name})
        # data = {
        #     'ids': self.ids,
        #     'names': names,
        # }
        # print(self.docteur_id.id)
        data = {
            'ids': self.ids,
            'form': {
                'docteur_id': self.docteur_id.id,
                'date': self.date,
            },
        }
        return self.env.ref('clinique.action_report_rdvs').report_action(self, data)

class AfficheRdvsPDF(models.AbstractModel):
    _name = 'report.clinique.report_rdvs'
    def _get_report_values(self, docids, data):
        print(data['form'])
        docs = self.env['clinique.rdv'].search(['&', '&', ('docteur', '=', int(data['form']['docteur_id'])), ('state', '=', 'confirmation'), ('date', '=', data['form']['date'])])
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

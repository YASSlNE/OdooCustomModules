# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Docteur(models.Model):
    _name = 'clinique.docteur'
    _description = 'Modele du docteur'

    name = fields.Char()
    date_docteur = fields.Date('Date de naissance', default=fields.Datetime.now)
    specialite = fields.Selection(
        [('cardiologie', 'Cardiologie'),
         ('reanimation', 'Réanimation'),
         ('urgence', 'Urgence')],
        'Spécialité')
    patient_id = fields.One2many('clinique.patient', 'docteur_id')
    state = fields.Selection([
        ('name', 'Name'),
        ('dateDeNaissance', 'Date de naissance'),
        ('specialite', 'Spécialité'),
    ], string='Status', readonly=True, default='name')
    # print(fields.Datetime.to_string(date_docteur))
    # print("---------------date---------------")
    # print(type(date_docteur))
    # print(date_docteur)
    # print("---------------date---------------")


class Patient(models.Model):
    _name = 'clinique.patient'
    _description = 'Modele du pati1ent'

    name = fields.Char()
    date_patient = fields.Date('Date de naissance', default=fields.Datetime.now)
    docteur_id = fields.Many2one('clinique.docteur')

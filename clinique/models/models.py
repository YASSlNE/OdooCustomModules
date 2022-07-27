# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

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
    age = fields.Integer(compute="calculate_age", readonly=True, store=True)
    def to_date(self):
        self.state = 'dateDeNaissance'
    def to_specialite(self):
        self.state =  'specialite'

    @api.depends('date_docteur')
    def calculate_age(self):
        today = date.today()
        self.age = today.year - self.date_docteur.year - ((today.month, today.day) < (self.date_docteur.month, self.date_docteur.day))
    # print(fields.Datetime.to_string(date_docteur))
    # print("---------------date---------------")
    # print(type(date_docteur))
    # print(date_docteur)
    # print("---------------date---------------")


class Patient(models.Model):
    _name = 'clinique.patient'
    _description = 'Modele du patient'
    name = fields.Char()
    date_patient = fields.Date('Date de naissance', default=fields.Datetime.now)
    docteur_id = fields.Many2one('clinique.docteur')
    age = fields.Integer(compute="calculate_age", store=True)
    state = fields.Selection([
        ('name', 'Name'),
        ('dateDeNaissance', 'Date de naissance'),
        ('docteur', 'Docteur'),
    ], string='Status', readonly=True, default='name')
    def to_date(self):
        self.state = 'dateDeNaissance'
    def to_docteur(self):
        self.state = 'docteur'

    @api.depends('date_patient')
    def calculate_age(self):
        today = date.today()
        self.age = today.year - self.date_patient.year - ((today.month, today.day) < (self.date_patient.month, self.date_patient.day))
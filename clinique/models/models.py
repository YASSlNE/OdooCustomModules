# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date




class Specialites(models.Model):
    _name = 'clinique.specialites'
    _description = 'Les spécialités des docteurs'
    name = fields.Char()


class Docteur(models.Model):
    _name = 'clinique.docteur'
    _description = 'Modele du docteur'
    name = fields.Char()
    date_docteur = fields.Date('Date de naissance', default=fields.Datetime.now)
    specialite = fields.Many2many('clinique.specialites')
    # specialiste = fields.Char(related = 'specialite_id.name')
    # patient_id = fields.One2many('clinique.patient', 'docteur_id')
    # state = fields.Selection([
    #     ('name', 'Name'),
    #     ('dateDeNaissance', 'Date de naissance'),
    #     ('specialite', 'Spécialité'),
    # ], string='Status', readonly=True, default='name')
    age = fields.Integer(compute="calculate_age", readonly=True, store=True)
    # def to_date(self):
    #     self.state = 'dateDeNaissance'
    # def to_specialite(self):
    #     self.state =  'specialite'

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
    # docteur_id = fields.Many2one('clinique.docteur')
    age = fields.Integer(compute="calculate_age", store=True)
    # state = fields.Selection([
    #     ('name', 'Name'),
    #     ('dateDeNaissance', 'Date de naissance'),
    #     ('docteur', 'Docteur'),
    # ], string='Status', readonly=True, default='name')
    # def to_date(self):
    #     self.state = 'dateDeNaissance'
    # def to_docteur(self):
    #     self.state = 'docteur'
    @api.depends('date_patient')
    def calculate_age(self):
        today = date.today()
        self.age = today.year - self.date_patient.year - ((today.month, today.day) < (self.date_patient.month, self.date_patient.day))


class RDV(models.Model):
    _name = 'clinique.rdv'
    _description = 'Les rendez vous'
    patient = fields.Many2one('clinique.patient')
    docteur = fields.Many2one('clinique.docteur')
    specialiste = fields.Many2many(related="docteur.specialite", readonly=True, relation = "clinique.specialites")
    # company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")

    date = fields.Date('Date du rendez vous', default=fields.Datetime.now)
    # specialite_patient = fields.Char(related='docteur.specialite', default="sdmlkfjsqdmfklj")
    sequence = fields.Char(string="Sequence", readonly=True,
                           required = True, copy = False, index = True,
                           default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('attendant', 'Attendant la confirmation du Docteur'),
        ('confirmation', 'Rendez vous confirmé'),
    ], string='state', readonly=True, default='draft')
    def patient_ready(self):
        self.state='attendant'
    def docteur_ready(self):
        self.state='confirmation'
    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence']= self.env['ir.sequence'].next_by_code('self.rdv') or 'New'
        result= super().create(vals)
        return result
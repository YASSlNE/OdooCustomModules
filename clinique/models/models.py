# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Docteur(models.Model):
    _name = 'clinique.docteur'
    _description = 'Modele du docteur'

    nom = fields.Char()
    prenom = fields.Char()
    age = fields.Integer()
    specialite = fields.Selection(
        [('cardiologie', 'Cardiologie'),
         ('reanimation', 'Réanimation'),
         ('urgence', 'Urgence')],
        'Spécialité')
    patient_id = fields.One2many('clinique.patient', 'docteur_id')


class Patient(models.Model):
    _name = 'clinique.patient'
    _description = 'Modele du pati1ent'

    nom = fields.Char()
    prenom = fields.Char()
    age = fields.Integer()
    docteur_id = fields.Many2one('clinique.docteur')
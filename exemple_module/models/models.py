# -*- coding: utf-8 -*-

from odoo import models, fields, api

#publishers
class exemple_module(models.Model):
    _name = 'exemple_module.exemple_module'
    _description = 'exemple_module.exemple_module'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    child_field_id=fields.One2many('exemple_module.exemple2', 'parent_field_id', String="Published books")

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100

#books
class exemple_module2(models.Model):
    _name = 'exemple_module.exemple2'
    _description = 'child model'
    name = fields.Char()
    value = fields.Integer()

    parent_field_id = fields.Many2one('exemple_module.exemple_module', String="Publisher")



    # child_field_id=fields.One2many('exemple_module.exemple_module', 'parent_field')
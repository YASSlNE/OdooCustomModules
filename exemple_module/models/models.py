# -*- coding: utf-8 -*-

from odoo import models, fields, api

#books
class exemple_module(models.Model):
    _name = 'exemple_module.exemple_module'
    _description = 'exemple_module.exemple_module'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    parent_field_id = fields.Many2one('exemple_module.exemple2', String="Publisher")

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100

#publisher
class exemple_module2(models.Model):
    _name = 'exemple_module.exemple2'
    _description = 'child model'
    name = fields.Char()
    value = fields.Integer()

    child_field_id=fields.One2many('exemple_module.exemple_module', 'parent_field_id', String="Published books")



    # child_field_id=fields.One2many('exemple_module.exemple_module', 'parent_field')
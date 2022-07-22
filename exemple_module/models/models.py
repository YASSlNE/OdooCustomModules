# -*- coding: utf-8 -*-

from odoo import models, fields, api


class exemple_module(models.Model):
    _name = 'exemple_module.exemple_module'
    _description = 'exemple_module.exemple_module'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    parent_field=fields.Many2one('exemple_module.exemple2','child_field')

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

class exemple_module2(models.Model):
    _name = 'exemple_module.exemple2'
    _description = 'child model'

    name = fields.Char()
    value = fields.Integer()
    
    child_field=fields.One2many('exemple_module.exemple_module')
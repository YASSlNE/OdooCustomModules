# -*- coding: utf-8 -*-

from odoo import models, fields, api


class exemple_module2(models.Model):
    _name = 'exemple_module2.exemple_module2'
    _description = 'exemple_module2.exemple_module2'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta
import inspect
class ReleveDePresence(models.Model):
	_name = 'releve.presence'

	mission_id = fields.Many2one('ordre.mission')
	date_begin = fields.Date()
	date_end = fields.Date()
	employe_id = fields.Many2one('hr.employee', related='mission_id.employee_id', readonly=True)
	job_id = fields.Many2one('hr.job', related='employe_id.job_id', readonly=True)
	lines = fields.One2many('releve.presence.lines', 'parent')
	name = fields.Char(string="Sequence", readonly=True,
                            copy = False, index = True,
                           default=lambda self: _('New'))
	@api.model
	def create(self, values):
		def diff_month(d1, d2):
			return (d1.year - d2.year) * 12 + d1.month - d2.month
		
		if values.get('name', 'New') == 'New':
			values['name']= self.env['ir.sequence'].next_by_code('releve.presence.ref') or 'New'
			return super(ReleveDePresence, self).create(values)

class ReleveDePresenceLines(models.Model):
	_name = 'releve.presence.lines'
	parent = fields.Many2one('releve.presence')
	date = fields.Date()
	description = fields.Char()
	@api.onchange('date')
	def check_date_is_valid(self):
		if(self.date!=False):
			if(self.date<self.parent.date_begin or self.date>self.parent.date_end):
				raise exceptions.ValidationError("Date invalide")
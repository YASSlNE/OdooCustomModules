from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta
import inspect
class ReleveDePresence(models.Model):
	_name = 'releve.presence'
	mission_id = fields.Many2one('ordre.mission')
	date_begin = fields.Datetime()
	date_end = fields.Datetime()
	employe_id = fields.Many2one('hr.employee', related='mission_id.employee_id', readonly=True)
	job_id = fields.Many2one('hr.job', related='employe_id.job_id', readonly=True)
	lines = fields.One2many('releve.presence.lines', 'parent')

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
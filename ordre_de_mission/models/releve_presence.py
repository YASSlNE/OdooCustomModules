from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, timedelta
from dateutil.rrule import rrule, MONTHLY
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
	client_id = fields.Many2one('res.partner', related='mission_id.client_id', readonly=True)
	mois = fields.Char()
	@api.model
	def create(self, values):
		print("----------------------------------------------------------------------")
		date_begin_converted = datetime.strptime(values['date_begin'], "%Y-%m-%d")
		date_end_converted = datetime.strptime(values['date_end'], "%Y-%m-%d")
		dates = [dt.strftime("%B") for dt in rrule(MONTHLY, dtstart=date_begin_converted, until=date_end_converted)]
		values['mois'] = str(dates).replace("'","").replace("]","").replace("[","")
		if values.get('name', 'New') == 'New':
			values['name']= self.env['ir.sequence'].next_by_code('releve.presence.ref') or 'New'
			return super(ReleveDePresence, self).create(values)


	def months(self):
		records = self.env['releve.presence'].search([('id', '=', self.id)])
		mois = records['mois']
		mois_seperated = mois.split(',')
		return mois_seperated
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
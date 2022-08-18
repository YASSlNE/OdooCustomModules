from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
import inspect
class RapportIntervention(models.Model):
    _name = 'rapport.intervention'
    name = fields.Char("Name")


    mission_id = fields.Many2many('ordre.mission', domain="[('employee_id', 'in', employes), ('projet_id', '=', projet_id), ('client_id', '=', client_id)]")
    client_id = fields.Many2one('res.partner')
    projet_id = fields.Many2one('project.project')
    date_begin = fields.Datetime()
    date_end = fields.Datetime()
    employes = fields.Many2many('hr.employee')
    clients = fields.Many2many('res.partner', domain="[('parent_id', '=', client_id)]" )
    line_t_ids = fields.One2many('rapport.intervention.lines.taches', 'rit_id')


    # @api.onchange('projet_id')
    # def fn(self):
    #     print("-------------------------------------")
    #     print(self.projet_id._ids)
    #     print("-------------------------------------")


    # @api.depends('employes2')
    # def _compute_employes(self):
    #     for line in self:
    #         line.employes=line.employes2._origin.id



    @api.model
    def create(self, values):
        print(f"the mission id is {values['mission_id']}")
        records = self.env['ordre.mission'].search([('id', '=', values['mission_id'])])
        records.ensure_one()
        dateLimitMin = datetime.strftime(records['heureDebut'], "%Y-%m-%d")
        dateLimitMax = datetime.strftime(records['heureFin'], "%Y-%m-%d")


        # conversion des dates
        dateInputMinConverted = datetime.strptime(values['date_begin'], "%Y-%m-%d %H:%M:%S")
        dateInputMaxConverted = datetime.strptime(values['date_end'], "%Y-%m-%d %H:%M:%S")


        dateInputMin = datetime.strftime(dateInputMinConverted, "%Y-%m-%d")
        dateInputMax = datetime.strftime(dateInputMaxConverted, "%Y-%m-%d")
        if(dateInputMin<dateLimitMin or rdateInputMax>dateLimitMax):
            raise exceptions.ValidationError("Intervale des dates invalide")
        else:
            duree = dateInputMaxConverted-dateInputMinConverted+timedelta(days=1)
            values['duree'] = duree
            res = super(RapportIntervention, self).create(values)
            return res


class RapportInterventionLinesTaches(models.Model):
    _name = 'rapport.intervention.lines.taches'
    rit_id = fields.Many2one('rapport.intervention')
    description = fields.Char()
    status = fields.Selection([('E', 'En cours'), ('C', 'Clôturé')])
    employes = fields.Many2one('hr.employee')


class StoreEmployees(models.Model):
    _name = 'rapport.store.employees'
    name = fields.Char()    
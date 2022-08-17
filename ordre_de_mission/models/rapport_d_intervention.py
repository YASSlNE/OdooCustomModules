from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class RapportIntervention(models.Model):
    _name = 'rapport.intervention'
    name = fields.Char("Name")
    mission_id = fields.Many2one('ordre.mission')
    client_id = fields.Many2one('res.partner', related = 'mission_id.client_id')
    projet_id = fields.Many2one('ordre.de.mission.projet', related = 'mission_id.projet_id')
    date_begin = fields.Datetime()
    date_end = fields.Datetime()
    duree = fields.Char()
    line_e_ids = fields.One2many('rapport.intervention.lines.employes', 'rie_id')
    line_c_ids = fields.One2many('rapport.intervention.lines.clients', 'ric_id')
    line_t_ids = fields.One2many('rapport.intervention.lines.taches', 'rit_id')
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
        if(dateInputMin<dateLimitMin or dateInputMax>dateLimitMax):
            raise exceptions.ValidationError("Intervale des dates invalide")
        else:
            duree = dateInputMaxConverted-dateInputMinConverted+timedelta(days=1)
            values['duree'] = duree
            res = super(RapportIntervention, self).create(values)
            return res


class RapportInterventionLinesEmployes(models.Model):
    _name = 'rapport.intervention.lines.employes'
    rie_id = fields.Many2one('rapport.intervention')
    employes = fields.Many2one('hr.employee', string="Employés")
class RapportInterventionLinesClients(models.Model):
    _name = 'rapport.intervention.lines.clients'
    ric_id = fields.Many2one('rapport.intervention')
    clients = fields.Many2one('res.partner', string="Clients") 
class RapportInterventionLinesTaches(models.Model):
    _name = 'rapport.intervention.lines.taches'
    rit_id = fields.Many2one('rapport.intervention')
    description = fields.Char()
    status = fields.Selection([('E', 'En cours'), ('C', 'Clôturé')])
    rie_related = fields.Many2one('rapport.intervention.lines.employes')
    employes = fields.Many2one(relation='hr.employee', related='rie_related.employes')
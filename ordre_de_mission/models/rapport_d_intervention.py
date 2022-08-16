from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class RapportIntervention(models.Model):
    _name = 'rapport.intervention'
    mission_id = fields.Many2one('ordre.mission')
    client_id = fields.Many2one('res.partner', related = 'mission_id.client_id')
    projet_id = fields.Many2one('ordre.de.mission.projet', related = 'mission_id.projet_id')
    date_begin = fields.Datetime()
    date_end = fields.Datetime()
    duree = fields.Char()
    display_type = fields.Selection([

       ( 'line_section' , "Section" ) ,

       ( 'line_note' , "Note" )] , default = False , help = "Technical field for UX purpose." )
    ri_id = fields.Many2one('rapport.intervention.lines')


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


class RapportInterventionLines(models.Model):
    _name = 'rapport.intervention.lines'
    name = fields.Char("Name")
    line_ids = fields.One2many('rapport.intervention', 'ri_id')
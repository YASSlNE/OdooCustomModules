from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta
import inspect
class RapportIntervention(models.Model):
    _name = 'rapport.intervention'
    # name = fields.Char("Name")


    mission_id = fields.Many2many('ordre.mission', domain="[('employee_id', 'in', employes), ('projet_id', '=', projet_id), ('client_id', '=', client_id)]")
    client_id = fields.Many2one('res.partner')
    projet_id = fields.Many2one('project.project')
    date_begin = fields.Datetime(required=True)
    date_end = fields.Datetime(required=True)
    employes = fields.Many2many('hr.employee', default=False)
    clients = fields.Many2many('res.partner', domain="[('parent_id', '=', client_id)]" )
    line_t_ids = fields.One2many('rapport.intervention.lines.taches', 'rit_id')

    duree = fields.Char()
    name = fields.Char(string="Sequence", readonly=True,
                           required = True, copy = False, index = True,
                           default=lambda self: _('New'))
    


    # @api.onchange('mission_id')
    # def missions(self):
    #     def intersection(list1, list2):  #Retourne l'intersection entre deux listes
    #         return list(set(list1) & set(list2))
    #     # for k in self.mission_id.ids:
    #     #     print(k)
    #     records = self.env['ordre.mission'].search([('id', 'in', self.mission_id.ids)])
    #     # for i in inspect.getmembers(records):
    #     #     if not i[0].startswith('_'):
    #     #         if not inspect.ismethod(i[1]): 
    #     #             print(i)
    #     employee_ids = []
    #     for r in records:
    #         employee_ids.append(r['employee_id'].id)
    #     print(f"employee ids are {employee_ids}")
    #     print(self.employes.ids)
    #     if(len(self.employes.ids)!=len(intersection(self.employes.ids, employee_ids))):
    #         print("ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")        

    @api.model
    def create(self, values):
        print(f"the mission id is {values['mission_id'][0][2]}")
        records = self.env['ordre.mission'].search([('id', 'in', values['mission_id'][0][2])])


        dateInputMinConverted = datetime.strptime(values['date_begin'], "%Y-%m-%d %H:%M:%S")
        dateInputMaxConverted = datetime.strptime(values['date_end'], "%Y-%m-%d %H:%M:%S")


        def CheckDatesValidation(record):
            dateLimitMin = datetime.strftime(record['heureDebut'], "%Y-%m-%d")
            dateLimitMax = datetime.strftime(record['heureFin'], "%Y-%m-%d")

            # conversion des dates

            dateInputMin = datetime.strftime(dateInputMinConverted, "%Y-%m-%d")
            dateInputMax = datetime.strftime(dateInputMaxConverted, "%Y-%m-%d")
            return (dateInputMin<dateLimitMin or dateInputMax>dateLimitMax)

        def not_intersection(list1, list2):
            return list(set(list1) ^ set(list2))
        def intersection(list1, list2):  #Retourne l'intersection entre deux listes
            return list(set(list1) & set(list2))
        # for k in self.mission_id.ids:
        #     print(k)
        # records2 = self.env['ordre.mission'].search([('id', 'in', self.mission_id.ids)])
        # # for i in inspect.getmembers(records):
        # #     if not i[0].startswith('_'):
        # #         if not inspect.ismethod(i[1]): 
        # #             print(i)
        employee_ids = [] #liste des employés qui sont dans les missions sélectionnés
        for r in records:  
            employee_ids.append(r['employee_id'].id)
        # print(f"employee ids are {employee_ids}")
        # print(self.employes.ids)
        # return super(RapportIntervention, self).create(values)
        employee_ids_selected = values['employes'][0][2]
        Error = False
        for r in records:
            Error=CheckDatesValidation(r)
            if(Error):
                break

        # if(dateInputMin<dateLimitMin or dateInputMax>dateLimitMax):
        #     raise exceptions.ValidationError("Intervale des dates invalide")
        # else:
        #     duree = dateInputMaxConverted-dateInputMinConverted+timedelta(days=1)
        #     values['duree'] = duree
        #     res = super(RapportIntervention, self).create(values)
        #     return res
        # print(employee_ids_selected)

        # print(employee_ids)
        # print(intersection(employee_ids_selected, employee_ids))
        print(f"Error value {Error}")
        if(len(employee_ids_selected)!=len(intersection(employee_ids_selected, employee_ids))):
            ErrorCausedBy = not_intersection(employee_ids_selected, employee_ids)
            ErrorCausedByNames = []
            getNames = self.env['hr.employee'].search([('id', 'in', ErrorCausedBy)])
            for r in getNames:
                print("qskldjfhlqsdk")
                ErrorCausedByNames.append(r.name)
            raise exceptions.ValidationError(f"Les missions de {ErrorCausedByNames} ne sont pas inclus")
        elif(Error):
            raise exceptions.ValidationError(f"L'intervalle des dates d'un rapport d'intervention doit être dans l'intersection des dates des ordres de mission sélectionnés")
        else:
            duree = dateInputMaxConverted-dateInputMinConverted+timedelta(days=1)
            values['duree'] = duree
            if values.get('name', 'New') == 'New':
                values['name']= self.env['ir.sequence'].next_by_code('rapport.intervention.ref') or 'New'
            res = super(RapportIntervention, self).create(values)
            return res

class RapportInterventionLinesTaches(models.Model):
    _name = 'rapport.intervention.lines.taches'
    rit_id = fields.Many2one('rapport.intervention')
    description = fields.Char()
    status = fields.Selection([('E', 'En cours'), ('C', 'Clôturé')])
    employes = fields.Many2one('hr.employee')
    @api.onchange('employes')
    def fn(self):
        if((self.employes.id not in self.rit_id.employes.ids) and (self.employes.id!=False)):
            raise exceptions.ValidationError(f"L'employé doit être un des employés choisi")
            
class StoreEmployees(models.Model):
    _name = 'rapport.store.employees'
    name = fields.Char()
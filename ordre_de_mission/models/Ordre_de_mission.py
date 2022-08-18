# -*- coding:utf-8 -*-
from odoo import models, fields, api, exceptions
# from openerp.exceptions import except_orm, Warning, RedirectWarning
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import calendar

# class Projet(models.Model):
#     _name = "ordre.de.mission.projet"
#     name = fields.Char()


class LieuCree(models.Model):
    _name = "lieu.cree"
    _description = "Lieu dont la mission est crée"
    name = fields.Char()


class LieuDeMission(models.Model):
    _name = "lieu.mission"
    _description = "Le lieu de la mission"
    name = fields.Char()


class ordre_mission(models.Model):
    _name = 'ordre.mission'
    _inherit = 'mail.thread'
    _description = "Creation des demandes d'ordre de mission"

    @api.model
    def _employee_get(self):
        print('self.env.uid==', self.env.uid)
        test = self.env.uid
        print(test, 'teeest')
        ids = self.env['hr.employee'].search([('user_id', '=', test)])
        print('ids==', ids)

    # return ids[0]

    # @api.multi
    def _visibility_note_chef(self):
        for demande in self:
            if demande.employee_id.parent_id.user_id.id == self.env.uid or demande.employee_id.coach_id.user_id.id == self.env.uid or self.env.uid == 1:
                demande.visibility_note_chef = True
            # return True
            else:
                demande.visibility_note_chef = False
            # return False

    # @api.multi
    def _required_note_chef(self):
        for demande in self:
            if demande.employee_id.user_id.id == self.env.uid:
                demande.required_note_chef = False
            # return True
            else:
                demande.required_note_chef = True
            # return False

    # @api.multi
    def _visibility_note_resp(self):
        for demande in self:
            if demande.employee_id.coach_id.user_id.id == self.env.uid or self.env.uid == 1:
                demande.visibility_note_resp = True
            # return True
            else:
                demande.visibility_note_resp = False
            # return False

    # @api.multi
    def _visibility_button_modifier(self):
        for demande in self:
            if demande.employee_id.user_id.id == self.env.uid:
                demande.visibility_button_modifier = True
            else:
                demande.visibility_button_modifier = False

    @api.depends('heureFin', 'heureDebut')
    def _calculer_interval(self):
        if (self.heureDebut and self.heureFin):
            heure_Debut = datetime.strptime(str(self.heureDebut), "%Y-%m-%d %H:%M:%S")
            heure_Fin = datetime.strptime(str(self.heureFin), "%Y-%m-%d %H:%M:%S")
            interval = heure_Fin - heure_Debut
            self.intervalAut = str(interval)

    # N°000 / 2022 for example
    name = fields.Char(string="Reference", default="/", readonly=True)
    dateCreate = fields.Date(default=fields.Date.today, string="Creation Date", readonly=True)
    # lieuCreate = fields.Selection([('Ssssejnene', 'Tunsssis'), ('Ssssejnene', 'Ssssfax'), ('Ssssejnene', 'Ssssejnene'), ], default='Tunis')
    lieuCree = fields.Many2one('lieu.cree')
    lieuDestination = fields.Many2one('lieu.mission', string="Destination")
    visibility_button_modifier = fields.Boolean(compute='_visibility_button_modifier', method=True)
    visibility_note_chef = fields.Boolean(compute='_visibility_note_chef', method=True)
    visibility_note_resp = fields.Boolean(compute='_visibility_note_resp', method=True)
    required_note_chef = fields.Boolean(compute='_required_note_chef', method=True)
    employee_id = fields.Many2one('hr.employee', string="Name and last name", required=True, default=_employee_get,
                                  states={'envoyer': [('readonly', True)], 'modifier': [('readonly', True)],
                                          'confirmerA': [('readonly', True)], 'confirmerV': [('readonly', True)],
                                          'imprimer': [('readonly', True)], 'archiver': [('readonly', True)],
                                          'refuser': [('readonly', True)],
                                          'annuler': [('readonly', True)]})  # ,readonly=True)
    # job = fields.Char(string='Titre du poste',related='employee_id.job_id', readonly=True)
    heureDebut = fields.Datetime(default=datetime.now(), required=True, readonly=True, states={'draft': [('readonly', False)], 'modifier': [
        ('readonly', False)]})  # string="De")
    heureFin = fields.Datetime(required=True, readonly=True, states={'draft': [('readonly', False)],
                                                                     'modifier': [('readonly', False)]})  # string="A")

    # , 'envoyer':[('readonly', False)]}

    destination = fields.Char(string = "Destination", required=True, readonly=True, states={'draft':[('readonly',False)]})

    projet_id = fields.Many2one('project.project', string = "Project")

    client_id = fields.Many2one('res.partner')
    # destination_state_id = fields.Many2one("res.country.state", required=True, readonly=True,
    #                                        states={'draft': [('readonly', False)], 'modifier': [('readonly', False)]})
    # destination_country_id = fields.Many2one('res.country', required=True, readonly=True,
    #                                          states={'draft': [('readonly', False)], 'modifier': [('readonly', False)]})

    objet_de_mission = fields.Text(string="Mission object", required=True, readonly=True,
                              states={'draft': [('readonly', False)]})
    transport = fields.Selection([('Vehicule Personel', "Vehicule Personel"), ('Autre', "Autre"), ], 'Transport',
                                 required=True, readonly=True, states={'draft': [('readonly', False)]})
    autre_moyen = fields.Char()
    matriculeVoit = fields.Char(string="Registration", readonly=True, states={'draft': [('readonly', False)]})
    precision = fields.Text(string="Note", readonly=True, states={'draft': [('readonly', False)]})
    note_chef = fields.Text(string="Team Leader Note", readonly=True,
                            states={'confirmerA': [('readonly', True)], 'envoyer': [('readonly', False)]})
    note_responsable = fields.Text(string="Note Responsible", readonly=True,
                                   states={'confirmerA': [('required', True), ('readonly', False)],
                                           'envoyer': [('required', False), ('readonly', True)]})
    intervalAut = fields.Char(string="Number of hours", readonly=True, compute='_calculer_interval', default="00:00:00",
                              store=True)

    user_id = fields.Many2one(related='employee_id.user_id', string='User', store=True)
    department_id = fields.Many2one(related='employee_id.department_id', string='Department', store=True)
    ##related field
    chef_id = fields.Many2one(related='employee_id.parent_id', string='Head team', store=True)
    date_aut_aff = fields.Char(string="Date Autorisation", store=True)

    state = fields.Selection([('draft', "In creation"),
                              ('annuler', "Cancel"),
                              ('modifier', "Waiting for change"),
                              ('envoyer', "Waiting validation1"),
                              ('confirmerA', "Waiting validation2"),
                              ('confirmerV', "Waiting to print"),
                              ('imprimer', "Waiting for signature and attachment"),
                              ('archiver', "Archive"),
                              ('refuser', "Refuser"), ], string="State", default='draft', track_visibility='onchange',
                             copy=False, )

    # @api.multi
    def action_draft(self):
        self.state = 'draft'

    # @api.multi
    def s_retour1(self):
        self.state = 'modifier'

    # @api.cr_uid_ids_context
    # @api.multi
    def s_envoyer(self):
        # self.state = 'envoyer'
        duree = timedelta(hours=0)
        print(duree)
        heure_Debut = datetime.strptime(str(self.heureDebut), "%Y-%m-%d %H:%M:%S")
        print(heure_Debut)
        heure_Fin = datetime.strptime(str(self.heureFin), "%Y-%m-%d %H:%M:%S")
        print(heure_Fin)
        interval = heure_Fin - heure_Debut
        print(interval)
        self.interval_c = str(interval)

        if interval >= duree:
            for demande in self:
                # demande_id = demande['id']
                # print(demande_id)

                ################################################
                mail_vals = {
                    'body': '<html> Demande d\'ordre de mission envoyer </html>',
                    'record_name': "Demande d'ordre de mission",
                    # 'res_id':ids[0],
                    # 'res_id': 1,
                    'reply_to': self.env['res.users'].sudo().browse().name,
                    'author_id': self.env['res.users'].sudo().browse().partner_id.id,
                    'model': 'ordre.mission',
                    'email_from': self.env['res.users'].sudo().browse().name,
                    'starred': True,
                }
                message = self.env['mail.message'].sudo().create(mail_vals)
                print("message", message)
                mail_notif_vals = {

                    'res_partner_id': self.env['res.users'].sudo().browse(self.employee_id.user_id.id).partner_id.id,

                    'mail_message_id': message.id,
                    'is_read': False,
                    # 'starred': True,

                }
                self.env['mail.notification'].sudo().create(mail_notif_vals)
            # self.state = 'envoyer'

            self.sudo().write({'state': 'envoyer'})
        # return True
        else:
            raise exceptions.ValidationError("Il faut selectioner la durée de la mission")

    # @api.multi
    def s_retour2(self):
        self.state = 'modifier'

    #######################################################"

    ####################################################"

    # @api.one
    def s_annuler(self):
        # self.state = 'annuler'
        for annuler in self:
            # annuler_id=annuler['id']

            mail_vals = {
                'body': '<html> La demande d\'ordre de mission est annulée  </html>',
                'record_name': "Demande d'ordre de mission annulée",
                # 'res_id':annuler.id,
                # 'res_id': 1,

                'reply_to': self.env['res.users'].sudo().browse().name,
                'author_id': self.env['res.users'].sudo().browse().partner_id.id,
                'model': 'ordre.mission',
                'email_from': self.env['res.users'].sudo().browse().name,
                'starred': True,
            }
            message = self.env['mail.message'].sudo().create(mail_vals)
            print("message", message)
            # annul = self.env['res.users'].browse(annuler_id).partner_id.id
            # print(annul, "annuler messg")

            mail_notif_emp_vals = {

                # 'res_partner_id':self.env['res.users'].browse(annuler_id).partner_id.id,

                'res_partner_id': self.env['res.users'].sudo().browse(annuler.employee_id.user_id.id).partner_id.id,

                # 'res_partner_id': self.env['res.users'].browse(self.employee_id.user_id.id).partner_id.id,

                'mail_message_id': message.id,
                'is_read': False,
                # 'starred': True,
            }

            print(mail_notif_emp_vals, "mail_notif_emp_vals")

            self.env['mail.notification'].sudo().create(mail_notif_emp_vals)
        # self.state = 'annuler'
        self.sudo().write({'state': 'annuler'})
        return True

    ################demande de modification ##########

    # @api.multi
    # def s_modifier(self):
    # 	self.state = 'modifier'

    ###########################"

    # @api.one
    def s_confirmer_A(self):
        # self.state = 'confirmerA'

        for confirm in self:
            mail_vals = {
                'body': "<html> Demande d'ordre de mission confirmée par le chef d'équipe</html>",
                'record_name': "Confirmation du chef d'équipe",
                'res_id': confirm.id,
                'reply_to': self.env['res.users'].browse().name,
                'author_id': self.env['res.users'].browse().partner_id.id,
                'model': 'ordre.mission',
                'email_from': self.env['res.users'].browse().name,
                'starred': True,
            }
            message = self.env['mail.message'].create(mail_vals)
            print(message, 'message')

            mail_notif_dep_vals = {
                # modif mromdhan: coach_id
                'res_partner_id': self.env['res.users'].browse(confirm.employee_id.coach_id.user_id.id).partner_id.id,

                'mail_message_id': message.id,
                'is_read': False,
                # 'starred': True,
            }
            self.env['mail.notification'].create(mail_notif_dep_vals)

            mail_notif_emp_vals = {

                'res_partner_id': self.env['res.users'].browse(confirm.employee_id.user_id.id).partner_id.id,
                'mail_message_id': message.id,
                'is_read': False,
                # 'starred': True,
            }
            self.env['mail.notification'].create(mail_notif_emp_vals)
        self.state = 'confirmerA'
        # self.write({'state': 'confirmerA'})
        # return True
        rep_chef = 'confirmerA'
        print("rep chef*********************", rep_chef)

    ##############################"""

    # @api.one
    def s_confirmer_V(self):
        # self.state = 'confirmerV'
        #
        for valid in self:
            mail_vals = {
                'body': "<html>Demande d'ordre de mission validée chef de département envoyer  </html>",
                'record_name': 'Validation du responsable département',
                'res_id': valid.id,
                'reply_to': self.env['res.users'].browse().name,
                'author_id': self.env['res.users'].browse().partner_id.id,
                'model': 'ordre.mission',
                'email_from': self.env['res.users'].browse().name,
                'starred': True,
            }
            message = self.env['mail.message'].create(mail_vals)

            mail_notif_emp_vals = {

                'res_partner_id': self.env['res.users'].browse(valid.employee_id.user_id.id).partner_id.id,
                # 'partner_id': self.env['res.users'].browse(valid.employee_id.user_id.id).partner_id.id,
                'mail_message_id': message.id,
                'is_read': False,
                # 'starred': True,
            }
            self.env['mail.notification'].create(mail_notif_emp_vals)
        self.state = 'confirmerV'

    # @api.multi
    def s_imprimer(self):
        self.state = 'imprimer'

    # @api.multi
    def s_archiver(self):
        self.state = 'archiver'

    # @api.one
    def s_refuser(self):
        # self.state = 'refuser'

        for refus in self:
            # refus_id=refus['id']
            mail_vals = {
                'body': '<html> La demande d\'ordre de mission est refusé  </html>',
                'record_name': "Demande d'ordre de mission refusée",
                # 'res_id':refus.id,
                'reply_to': self.env['res.users'].sudo().browse().name,
                'author_id': self.env['res.users'].sudo().browse().partner_id.id,
                'model': 'ordre.mission',
                'email_from': self.env['res.users'].sudo().browse().name,
                'starred': True,
            }
            message = self.env['mail.message'].sudo().create(mail_vals)

            mail_notif_emp_vals = {

                # 'partner_id':self.env['res.users'].browse(refus.employee_id.user_id.id).partner_id.id,
                # 'res_partner_id': self.env['res.users'].browse(refus_id).partner_id.id,
                'res_partner_id': self.env['res.users'].sudo().browse(refus.employee_id.user_id.id).partner_id.id,

                'mail_message_id': message.id,
                'is_read': False,
                # 'starred': True,
            }
            self.env['mail.notification'].sudo().create(mail_notif_emp_vals)
        # self.state = 'refuser'
        self.sudo().write({'state': 'refuser'})
        return True

    @api.onchange('heureDebut')
    def _modifier_date(self):
        self.heureFin = self.heureDebut
        print("self.heureFin....................", self.heureFin)
        if self.heureDebut:
            date_x = datetime.strptime(str(self.heureDebut), "%Y-%m-%d %H:%M:%S")
            print("date_x*********************", date_x)
            self.date_aut_aff = datetime.strftime(date_x, "%Y-%m-%d")
            print("self.date_aut_aff*********************", self.date_aut_aff)

    def reset_sequence(self):
        sequences = self.env['ir.sequence'].search([('name', '=like', 'Ordre Mission')])
        sequences.write({'number_next': 1})
        return None

    @api.model
    def create(self, values):
        duree = timedelta(hours=0)
        debut = values.get('heureDebut', False)
        heure_Debut = datetime.strptime(debut, "%Y-%m-%d %H:%M:%S")
        fin = values.get('heureFin', False)
        heure_Fin = datetime.strptime(fin, "%Y-%m-%d %H:%M:%S")
        interval = heure_Fin - heure_Debut
        values['intervalAut'] = str(interval)
        date_xxx = datetime.strftime(heure_Debut, "%Y-%m-%d")
        print("self.date_aut_aff*********************", date_xxx)
        values['date_aut_aff'] = str(date_xxx)
        date_now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        date_from = datetime.strftime(heure_Debut, "%Y-%m-%d %H:%M:%S")
        print("date_now*********************", date_now)
        print("date_from*********************", date_from)





        if date_from < date_now:
            raise exceptions.ValidationError(
                "Vous ne pouvez pas créer une demande d'ordre de mission avant " + date_now + " !")

        if interval >= duree:

            name = values.get('name', False)
            employee_id = values.get('employee_id', False)
            employee = self.env['hr.employee'].browse(employee_id)
            seq_miss_company = self.env['ir.sequence'].search(
                [('company_id', '=', employee.company_id.id), ('code', '=', 'ord.miss.ref'),
                 ('name', '=', 'Ordre Mission')])
            # values['name'] = self.env['ir.sequence'].next_by_id(seq_miss_company.id)
            # contract_id = super(hr_contract, self).create( vals)
            values['name'] = self.env['ir.sequence'].get('ord.miss.ref') or ' '
            print(values['name'])
            res = super(ordre_mission, self).create(values)
            return res
        else:
            raise exceptions.ValidationError("Il faut selectioner la durée de la mission")

